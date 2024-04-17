from flask import render_template, request, redirect, url_for, session, jsonify, Blueprint, flash, send_from_directory
from app import app
from flask_mysqldb import MySQL
from views.dbrequest import DatabaseRequest
from flask_bcrypt import Bcrypt
from markupsafe import escape
import os
import cv2
import face_recognition
import numpy as np
import base64
from functools import wraps 
from datetime import date, timedelta, datetime, time
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from PIL import Image
from werkzeug.utils import secure_filename
import io
import uuid
import random
import json

app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}
app.secret_key = "ITSASECRET"
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nexushrdb'
app.config['UPLOAD_REFERENCE_PHOTO'] = 'static/uploads/reference_image'
app.config['UPLOAD_EDUCATION_ATTACHMENT'] = 'static/uploads/user_education_attachment'
app.config['UPLOAD_CLAIM_ATTACHMENT'] = 'static/uploads/user_claim_attachment'
app.config['UPLOAD_LEAVES_ATTACHMENT'] = 'static/uploads/user_leaves_attachment'
app.config['UPLOAD_SERVICE_DESK_ATTACHMENT'] = 'static/uploads/user_service_desk_attachment'
app.config['TESTER'] = 'static/uploads/tester'
app.config['PROFILE_FOLDER'] = 'static/uploads/profile_photos'
app.config['USER_PAYSLIP'] = 'static/uploads/user_payslip'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

app.config['STAFF_TIME_IN'] = datetime.strptime('08:00:00', '%H:%M:%S').time()
app.config['STAFF_TIME_OUT'] = datetime.strptime('17:00:00', '%H:%M:%S').time()

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mysql = MySQL(app)
db_request = DatabaseRequest(mysql)

#------------------------------------- Safe Guard Admin -------------------------------------#
def requires_authentication_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated
#----------------------------------- End Of Safe Guard Admin ---------------------------------#

@app.route('/')
def index():
    return redirect(url_for('admin.login_register'))

#------------------------------ Admin Blueprint -------------------------------#
admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.route('/login-register', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        if 'login-button' in request.form:
            username = request.form.get('input-login-username')
            password = request.form.get('input-login-password')
            companyCode = request.form.get('input-login-company-code')
            
            if all([username, password, companyCode]):
                admin_detail = db_request.get_detail('LOGIN_ADMIN', (username, companyCode,))
                
                if admin_detail:
                    if bcrypt.check_password_hash(admin_detail['adminPassword'], password):
                        session['admin_id'] = admin_detail['adminId']
                        session['company_code'] = admin_detail['adminCompanyId']
                        return redirect(url_for('admin.register_staff'))
                    else:
                        flash('Wrong Password or Username!', 'danger')
                        return redirect(url_for('admin.login_register'))
                else:
                    flash('Username or company code not found!', 'danger')
                    return redirect(url_for('admin.login_register'))
                
            
        elif 'register-button' in request.form:
            fullname = request.form.get('input-register-fullname')
            username = request.form.get('input-register-username')
            password = request.form.get('input-register-password')
            company_name = request.form.get('input-register-company-name')
            company_code = request.form.get('input-register-company-code-hidden')

            if all([fullname, username, password, company_name, company_code]):
                
                if db_request.get_detail('CHECK_ADMIN_USERNAME', (username,)):
                    flash('Admin username already exists!', 'danger')
                    return redirect(url_for('admin.login_register'))
                else:
                    db_request.insert_data('INSERT_COMPANY', (company_name, company_code))
                    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    db_request.insert_data('INSERT_STAFF', (fullname, username, hashed_password, company_code))
                    flash(f'Admin Register successfully! Your Company Code is {company_code}', 'success')
                    return redirect(url_for('admin.login_register'))
            
    return render_template('/admin/login.html')

@app.route('/generate-company-code', methods=['GET'])
def generate_company_code():
    company_code = str(random.randint(10000, 99999))
    if db_request.get_detail('CHECK_COMPANY_CODE', (company_code,)):
        return generate_company_code()
    return company_code

@admin_blueprint.route('/dashboard', methods=['GET'])
@requires_authentication_admin
def dashboard():
    return render_template('/admin/test-dashboard.html')

@admin_blueprint.route('/leave-request', methods=['GET', 'POST'])
@requires_authentication_admin
def leave_request():
    if request.method == 'POST':
        leaveId = request.form.get('leaveId')
        if 'reject-button' in request.form:
            db_request.update_data('UPDATE_LEAVE', (leaveId, 'rejected'))
            flash('Leave request rejected!', 'danger')
            return redirect(url_for('admin.leave_request'))

        elif 'approve-button' in request.form:
            db_request.update_data('UPDATE_LEAVE', (leaveId, 'approved'))
            flash('Leave request approved!', 'success')
            return redirect(url_for('admin.leave_request'))

    get_all_leave = db_request.get_detail('GET_ALL_PENDING_LEAVES', (session['company_code'],))
    return render_template('/admin/leaves/leave-request.html', get_all_leave=get_all_leave)

@admin_blueprint.route('/leave-history', methods=['GET', 'POST'])
@requires_authentication_admin
def leave_history():
    get_all_leave = db_request.get_detail('GET_ALL_LEAVES', (session['company_code'],))
    return render_template('/admin/leaves/leave-history.html', get_all_leave=get_all_leave)

@admin_blueprint.route('/claim-request', methods=['GET', 'POST'])
@requires_authentication_admin
def claim_request():
    if request.method == 'POST':
        claimId = request.form.get('claimId')
        if 'reject-button' in request.form:
            db_request.update_data('UPDATE_CLAIM', (claimId, 'rejected'))
            flash('Claims request rejected!', 'danger')
            return redirect(url_for('admin.claim_request'))

        elif 'approve-button' in request.form:
            db_request.update_data('UPDATE_CLAIM', (claimId, 'approved'))
            flash('Claim request approved!', 'success')
            return redirect(url_for('admin.claim_request'))

    get_all_claims = db_request.get_detail('GET_ALL_PENDING_CLAIMS', (session['company_code'],))
    return render_template('/admin/claims/claim-request.html', get_all_claims=get_all_claims)

@admin_blueprint.route('/claim-history', methods=['GET', 'POST'])
@requires_authentication_admin
def claim_history():
    get_all_claims = db_request.get_detail('GET_ALL_CLAIMS', (session['company_code'],))
    return render_template('/admin/claims/claim-history.html', get_all_claims=get_all_claims)

@admin_blueprint.route('/register-staff', methods=['GET', 'POST'])
@requires_authentication_admin
def register_staff():
    if request.method == 'POST':
        userId = request.form.get('userId')
        fullName = request.form.get('userFullName')
        position = request.form.get('userPosition')
        race = request.form.get('userRace')
        nationality = request.form.get('userNationality')
        religion = request.form.get('userReligion')
        password = request.form.get('userPassword')
        refImage = ""
        if 'refImage' in request.files:
            refImage = request.files['refImage']

        if all([userId, fullName, position, race, nationality, religion, password, refImage]):

            if db_request.get_detail('CHECK_STAFF_ID', (userId,)):
                flash('Staff ID already exists!', 'danger')
                return redirect(url_for('admin.register_staff'))
            
            if allowed_file(refImage.filename):
                filename = userId + '.' + refImage.filename.rsplit('.', 1)[1].lower()
                refImage.save(os.path.join(app.config['UPLOAD_REFERENCE_PHOTO'], filename))
                refImage = filename
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                db_request.insert_data('INSERT_USERS', (userId, session['company_code'], fullName, position, race, nationality, religion, hashed_password, refImage))
                flash('Staff Registered Successfully!', 'success')
                return redirect(url_for('admin.register_staff'))

    return render_template('/admin/staff/register-staff.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_blueprint.route('/staff-list', methods=['GET', 'POST'])
@requires_authentication_admin
def staff_list():
    get_staff_list = db_request.get_detail('GET_STAFF_LIST', (session['company_code'],))
    return render_template('/admin/staff/staff-list.html', get_staff_list=get_staff_list)

@admin_blueprint.route('/staff-attendance', methods=['GET', 'POST'])
@requires_authentication_admin
def staff_attendance():
    get_staff_list = db_request.get_detail('GET_STAFF_LIST', (session['company_code'],))
    staff_detail = db_request.get_detail('GET_USER_ATTENDANCE', (int(1000),))
    return render_template('/admin/attendance/view-attendance.html', get_staff_list=get_staff_list, staff_detail=staff_detail)

@admin_blueprint.route('/announcement', methods=['GET', 'POST'])
@requires_authentication_admin
def announcement():
    if request.method == 'POST':    
        memoTo = request.form.getlist('memoTo')
        memoSubject = request.form.get('memoSubject')
        memoMessage = request.form.get('memoMessage')
        if all([memoTo, memoSubject, memoMessage]):
            for user in memoTo:
                db_request.insert_data('INSERT_ANNOUNCEMENT', (session['admin_id'],user, memoSubject, memoMessage, session['company_code']))
            flash('Announcement Sent Successfully!', 'success')
            return redirect(url_for('admin.announcement'))
    get_user = db_request.get_detail('GET_ALL_USER', (session['company_code'],))
    print(get_user)
    return render_template('/admin/announcement/announcement.html', get_user=get_user)

@admin_blueprint.route('/service-request', methods=['GET', 'POST'])
@requires_authentication_admin
def service_request():
    if request.method == 'POST':
        serviceId = request.form.get('serviceId')
        serviceNote = request.form.get('serviceNote')
       
        if all([serviceId, serviceNote]):
            db_request.update_data('UPDATE_SERVICE_DESK', (serviceId, serviceNote, 'done'))
            flash('Service request done !', 'success')
            return redirect(url_for('admin.service_request'))

    get_all_service = db_request.get_detail('GET_ALL_PENDING_SERVICE', (session['company_code'],))
    return render_template('/admin/service-desk/service-request.html', get_all_service=get_all_service)

@admin_blueprint.route('/service-history', methods=['GET', 'POST'])
@requires_authentication_admin
def service_history():
    get_service_history = db_request.get_detail('GET_ALL_SERVICE', (session['company_code'],))
    return render_template('/admin/service-desk/service-history.html', get_service_history=get_service_history)

@admin_blueprint.route('/report/<staff_id>/', methods=['GET', 'POST'])
@requires_authentication_admin
def report(staff_id):
    month = request.form.get('input-month')
    staff_detail = db_request.get_detail('GET_USER_DETAIL', (int(staff_id),))
    staff_attendance = db_request.get_detail('GET_USER_ATTENDANCE_REPORT', (int(staff_id), month))
    total_overtime_hours, late_days, early_days, overtime_days = calculate_attendance_metrics(staff_attendance)
    return render_template('/admin/report/report.html', 
                           staff_detail=staff_detail, 
                           staff_attendance=staff_attendance, 
                           month=month,
                           total_overtime_hours=total_overtime_hours,
                           late_days=late_days,
                           early_days=early_days,
                           overtime_days=overtime_days)

@admin_blueprint.route('/upload-payslip', methods=['POST'])
@requires_authentication_admin
def upload_payslip():
    staff_id = request.form.get('userId')
    payslip = request.files['payslip']
    month = request.form.get('input-month')
    if allowed_file(payslip.filename):
        _, ext = os.path.splitext(payslip.filename)
        filename = f"{staff_id}{ext}"
        payslip.save(os.path.join(app.config['USER_PAYSLIP'], filename))
        db_request.insert_data('INSERT_PAYSLIP', (staff_id, filename, month))
        flash('Payslip uploaded successfully!', 'success')
    return redirect(url_for('admin.staff_attendance'))

def calculate_attendance_metrics(attendance_records):
    total_overtime_hours = 0
    late_days = 0
    early_days = 0
    overtime_days = 0

    for record in attendance_records:
        total_overtime_hours += record['overtime']
        if record['attendanceStatus'] == 'late':
            late_days += 1
        elif record['attendanceStatus'] == 'early':
            early_days += 1
        if record['overtimeStatus'] == 'yes':
            overtime_days += 1

    return total_overtime_hours, late_days, early_days, overtime_days

@admin_blueprint.route('/logout', methods=['GET', 'POST'])
@requires_authentication_admin
def logout():
    return redirect(url_for('admin.login_register'))


app.register_blueprint(admin_blueprint)
#------------------------------ End Of Admin Blueprint -------------------------------#

#------------------------------ Authenticate Blueprint -------------------------------#
authenticateBP = Blueprint('authenticate', __name__, url_prefix='/authenticate')

@authenticateBP.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        staff_id = request.json['staffId']
        staff_password = request.json['password']
        companny_code = request.json['companycode']

        if all([staff_id, staff_password]):
            staff_detail = db_request.get_detail('LOGIN_STAFF', (staff_id, companny_code))
            if staff_detail:
                if bcrypt.check_password_hash(staff_detail['userPassword'], staff_password):
                    access_token = create_access_token(identity=staff_id)
                    return jsonify({'token': access_token, 'userid': staff_detail['userId']}), 200
                else:
                    return jsonify({'message': 'Wrong Password or Username!'}), 401
            else:
                return jsonify({'status': 'error', 'message': 'Username or Company Code not found!'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

app.register_blueprint(authenticateBP)

#------------------------------ End Of Authenticate Blueprint -------------------------------#

#------------------------------------ Service Blueprint -------------------------------------#
servicesBP = Blueprint('services', __name__, url_prefix='/services')

@servicesBP.route('/homepage', methods=['GET'])
@jwt_required()
def homepage():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        staff_id = request.args.get('staffId')
        if all([staff_id]):
            staff_detail = db_request.get_detail('HOME_PAGE', (staff_id,))
        
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

@servicesBP.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_REFERENCE_PHOTO'], filename)

@servicesBP.route('/personal-details', methods=['GET'])
@jwt_required()
def user_profile():
    if request.method == 'GET':
        staff_id = request.args.get('staffId')
        if all([staff_id]):
            staff_detail = db_request.get_detail('PERSONAL_DETAIL', (staff_id,))
        
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

@servicesBP.route('/user-address', methods=['GET', 'POST'])
@jwt_required()
def user_address():
    if request.method == 'GET':
        staff_id = request.args.get('staffId')
        if all([staff_id]):
            staff_detail = db_request.get_detail('GET_ADDRESS', (staff_id,))
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    if request.method == 'POST':
        staffId = get_jwt_identity()
        address1 = request.json['address1']
        address2 = request.json['address2']
        city = request.json['city']
        postcode = request.json['postcode']
        region = request.json['region']

        if all([address1, address2, city, postcode]):
            staff_detail = db_request.get_detail('GET_ADDRESS', (int(staffId),))
            if staff_detail:
                update_address = db_request.update_data('UPDATE_ADDRESS', (staffId, address1, address2, city, postcode, region))
                if update_address:
                    return jsonify({'message': 'Address update successfully!'}), 200
                else:
                    return jsonify({'message': 'Failed to update address!'}), 401
            else:
                insert_address = db_request.insert_data('INSERT_ADDRESS', (staffId, address1, address2, city, postcode, region))
                if insert_address:
                    return jsonify({'message': 'Address added successfully!'}), 200
                else:
                    return jsonify({'message': 'Failed to add address!'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

@servicesBP.route('/user-contact', methods=['GET', 'POST'])
@jwt_required()
def user_contact():
    if request.method == 'GET':
        staffId = get_jwt_identity()
        if all([staffId]):
            staff_detail = db_request.get_detail('GET_CONTACT', (int(staffId),))
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    if request.method == 'POST':
        staffId = get_jwt_identity()
        userEmail = request.json['userEmail']
        userPhone = request.json['userPhone']
        emergencyName = request.json['emergencyName']
        emergencyPhone = request.json['emergencyPhone']
        emergencyRelation = request.json['emergencyRelation']

        if all([staffId, userEmail, userPhone, emergencyName, emergencyPhone, emergencyRelation]):
            staff_detail = db_request.get_detail('GET_CONTACT', (int(staffId),))
            if staff_detail:
                update_address = db_request.update_data('UPDATE_CONTACT', (staffId, userEmail, userPhone, emergencyName, emergencyPhone, emergencyRelation))
                if update_address:
                    return jsonify({'message': 'Contact information update successfully!'}), 200
                else:
                    return jsonify({'message': 'Failed to update contact information!'}), 401
            else:
                insert_address = db_request.insert_data('INSERT_CONTACT', (staffId, userEmail, userPhone, emergencyName, emergencyPhone, emergencyRelation))
                if insert_address:
                    return jsonify({'message': 'Contact information added successfully!'}), 200
                else:
                    return jsonify({'message': 'Failed to add contact information!'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

@servicesBP.route('/user-education', methods=['GET', 'POST'])
@jwt_required()
def user_education():
    if request.method == 'GET':
        staffId = get_jwt_identity()
        if all([staffId]):
            staff_detail = db_request.get_detail('GET_EDUCATION', (int(staffId),))
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    if request.method == 'POST':
        staffId = get_jwt_identity()
        highestEducation = request.json['highestEducation']
        educationPlace = request.json['educationPlace']
        yearGraduation = request.json['yearGraduation']
        result = request.json['educationResult']
        attachment = request.json['attachment']

        if all([staffId, highestEducation, educationPlace, yearGraduation, result]):
            
            old_attachment = db_request.get_detail('OLD_EDUCATION', (staffId,))
            if old_attachment:
                filename = old_attachment['educationProof']

            if attachment is not None:
                userAttachment = base64.b64decode(attachment)
                image = Image.open(io.BytesIO(userAttachment))
                if image.format not in ['JPEG', 'PNG', 'JPG']:  
                    image = image.convert('RGB')

                if old_attachment:
                    os.remove(os.path.join(app.config['UPLOAD_EDUCATION_ATTACHMENT'], filename))

                random_filename = uuid.uuid4().hex + '.' + image.format.lower()
                filename = secure_filename(random_filename)

                image.save(os.path.join(app.config['UPLOAD_EDUCATION_ATTACHMENT'], filename))

            staff_detail = db_request.get_detail('GET_EDUCATION', (int(staffId),))
            if staff_detail:
                update_address = db_request.update_data('UPDATE_EDUCATION', (staffId, highestEducation, educationPlace, yearGraduation, result, filename))
                if update_address:
                    return jsonify({'message': 'Education information update successfully!'}), 200
                else:
                    return jsonify({'message': 'Failed to update Education information!'}), 401
            else:
                insert_address = db_request.insert_data('INSERT_EDUCATION', (staffId, highestEducation, educationPlace, yearGraduation, result, filename))
                if insert_address:
                    return jsonify({'message': 'Education information added successfully!'}), 200
                else:
                    return jsonify({'message': 'Failed to add Education information!'}), 401
                
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

@servicesBP.route('/serve-education-attachment/<filename>')
def serve_educationAttachment(filename):
    return send_from_directory(app.config['UPLOAD_EDUCATION_ATTACHMENT'], filename)

@servicesBP.route('/user-claim', methods=['GET', 'POST'])
@jwt_required()
def user_claims():
    if request.method == 'GET':
        staffId = get_jwt_identity()
        if all([staffId]):
            staff_detail = db_request.get_detail('GET_CLAIMS', (int(staffId),))
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    if request.method == 'POST':
        staffId = get_jwt_identity()
        claimGroupName = request.json['claimGroupName']
        claimName = request.json['claimName']
        receiptNo = request.json['receiptNo']
        receiptAmount = request.json['receiptAmount']
        attachment = request.json['attachment']

        if all([staffId, claimGroupName, claimName, receiptNo, receiptAmount, attachment]):
            if attachment is not None:
                userAttachment = base64.b64decode(attachment)
                image = Image.open(io.BytesIO(userAttachment))
                if image.format not in ['JPEG', 'PNG', 'JPG']:  
                    image = image.convert('RGB')
                random_filename = uuid.uuid4().hex + '.' + image.format.lower()
                filename = secure_filename(random_filename)
                image.save(os.path.join(app.config['UPLOAD_CLAIM_ATTACHMENT'], filename))
            
            insert_claim = db_request.insert_data('INSERT_CLAIM', (staffId, claimGroupName, claimName, receiptNo, receiptAmount, filename))
            if insert_claim:
                return jsonify({'message': 'Claim successfully applied !'}), 200
            else:
                return jsonify({'message': 'Failed to apply claim !'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

@servicesBP.route('/user-leave', methods=['GET', 'POST'])
@jwt_required()
def user_leaves():
    if request.method == 'GET':
        staffId = get_jwt_identity()
        if all([staffId]):
            staff_detail = db_request.get_detail('GET_LEAVES', (int(staffId),))
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    if request.method == 'POST':
        staffId = get_jwt_identity()
        leaveReason = request.json['leaveReason']
        leaveStart = request.json['leaveStart']
        leaveEnd = request.json['leaveEnd']
        leaveDuration = request.json['leaveDuration']
        attachment = request.json['attachment']

        if all([staffId, leaveReason, leaveStart, leaveEnd, leaveDuration, attachment]):
            if attachment is not None:
                userAttachment = base64.b64decode(attachment)
                image = Image.open(io.BytesIO(userAttachment))
                if image.format not in ['JPEG', 'PNG', 'JPG']:  
                    image = image.convert('RGB')
                random_filename = uuid.uuid4().hex + '.' + image.format.lower()
                filename = secure_filename(random_filename)
                image.save(os.path.join(app.config['UPLOAD_LEAVES_ATTACHMENT'], filename))
            
            insert_claim = db_request.insert_data('INSERT_LEAVE', (staffId, leaveReason, leaveStart, leaveEnd, leaveDuration, filename))
            if insert_claim:
                return jsonify({'message': 'Leave successfully applied !'}), 200
            else:
                return jsonify({'message': 'Failed to apply leave !'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

@servicesBP.route('/service-desk', methods=['GET', 'POST'])
@jwt_required()
def service_desk():
    if request.method == 'GET':
        staffId = get_jwt_identity()
        if all([staffId]):
            staff_detail = db_request.get_detail('GET_SERVICES_DESK', (int(staffId),))
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    if request.method == 'POST':
        staffId = get_jwt_identity()
        serviceProblem = request.json['serviceProblem']
        attachment = request.json['attachment']

        if all([staffId, serviceProblem, attachment]):
            if attachment is not None:
                userAttachment = base64.b64decode(attachment)
                image = Image.open(io.BytesIO(userAttachment))
                if image.format not in ['JPEG', 'PNG', 'JPG']:  
                    image = image.convert('RGB')
                random_filename = uuid.uuid4().hex + '.' + image.format.lower()
                filename = secure_filename(random_filename)
                image.save(os.path.join(app.config['UPLOAD_SERVICE_DESK_ATTACHMENT'], filename))
            
            insert_claim = db_request.insert_data('INSERT_SERVICE_DESK', (staffId, serviceProblem, filename))
            if insert_claim:
                return jsonify({'message': 'Service desk successfully applied !'}), 200
            else:
                return jsonify({'message': 'Failed to apply service desk !'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

def jsonify_timedelta(obj):
    if isinstance(obj, timedelta):
        return str(obj)  # Convert timedelta to string format
    elif isinstance(obj, date):
        return obj.isoformat()  # Convert date to ISO format
    raise TypeError(f'Object of type {type(obj)} is not JSON serializable')

@servicesBP.route('/user-attendance', methods=['GET', 'POST'])
@jwt_required()
def user_attendance():
    if request.method == 'GET':
        staffId = get_jwt_identity()
        if all([1]):
            staff_detail = db_request.get_detail('GET_USER_ATTENDANCE', (int(staffId),))
            if staff_detail:
                return json.dumps(staff_detail, default=jsonify_timedelta), 200, {'Content-Type': 'application/json'}
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    if request.method == 'POST':
        try:
            staffId = get_jwt_identity()
            get_staff_ref = db_request.get_detail('GET_REF_IMAGE', (staffId,))['userReference']
            data = request.json['userImage']
            nparr = np.frombuffer(base64.b64decode(data), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            reference_image = face_recognition.load_image_file(os.path.join(app.config['UPLOAD_REFERENCE_PHOTO'] , get_staff_ref))
            reference_encoding = face_recognition.face_encodings(reference_image)[0]
            
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare with the reference encoding
                matches = face_recognition.compare_faces([reference_encoding], face_encoding)
                if True in matches:
                    staff_current_time = datetime.now().time()
                    current_date = datetime.now().strftime("%Y-%m-%d")

                    # staff_current_time = time(21, 30)
                    # current_date = date(2024, 4, 2).strftime("%Y-%m-%d")

                    existing_attendance = db_request.get_detail('CHECK_ATTENDANCE', (staffId, current_date))
                    if existing_attendance:
                        if existing_attendance['overtimeStatus'] == 'unknown':
                            current_check_out = datetime.combine(datetime.today(), staff_current_time)
                            check_out_ref = datetime.combine(datetime.today(), app.config['STAFF_TIME_OUT'])
                            staff_check_out_late = current_check_out - check_out_ref
                            if staff_check_out_late > timedelta(hours=1):
                                hours_late = int(staff_check_out_late.total_seconds() / 3600)
                                overtime = str(hours_late)
                                attendance_detail =db_request.update_data('UPDATE_ATTENDANCE', (staffId, current_date, staff_current_time, overtime, 'yes'))
                                return jsonify(attendance_detail), 200
                            else:
                                attendance_detail =db_request.update_data('UPDATE_ATTENDANCE', (staffId, current_date, staff_current_time, '00:00', 'no'))
                                return jsonify(attendance_detail), 200
                        else:
                            return jsonify({"message": "User Already Checked In and Out Today!"}), 201

                    else:
                        if staff_current_time > app.config['STAFF_TIME_IN']:
                            current_check_in = datetime.combine(datetime.today(), staff_current_time)
                            check_in_ref = datetime.combine(datetime.today(), app.config['STAFF_TIME_IN'])
                            staff_check_in_late = current_check_in - check_in_ref
                            hours_late, remainder = divmod(staff_check_in_late.total_seconds(), 3600)
                            minutes_late = remainder // 60
                            time_late = f"{int(hours_late)}:{int(minutes_late)}"
                            attendance_detail = db_request.insert_data('INSERT_ATTENDANCE', (staffId, staff_current_time, time_late, 'late'))
                            return jsonify(attendance_detail), 200
                        else:
                            attendance_detail = db_request.insert_data('INSERT_ATTENDANCE', (staffId, staff_current_time, '00:00', 'on time'))
                            return jsonify(attendance_detail), 200
                        
            return jsonify({"message": "Face not recognized!"}), 400
        
        except Exception as e:
            print('Error: ', e)
            return jsonify({"message": "An error occurred!"}), 500

@servicesBP.route('/user-memo', methods=['GET', 'POST'])
@jwt_required()
def user_memo():
    if request.method == 'POST':
        memoId = request.json['memoId']

        if all([memoId]):
            db_request.update_data('UPDATE_MEMO', (memoId, 'read'))
            return jsonify({'message': 'Memo Sent Successfully!'}), 200
        

    if request.method == 'GET':
        staffId = get_jwt_identity()
        memoStatus = request.args.get('memoStatus')
        if all([staffId, memoStatus]):
            staff_detail = db_request.get_detail('GET_MEMO', (int(staffId), memoStatus))
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

@servicesBP.route('/user-payslip', methods=['GET'])
@jwt_required()
def user_payslip():
    if request.method == 'GET':
        staffId = get_jwt_identity()
        print(staffId)
        if all([staffId]):
            staff_detail = db_request.get_detail('GET_PAYSLIP', (int(staffId),))
            print(staff_detail)
            if staff_detail:
                return jsonify(staff_detail), 200
            else:
                return jsonify({'message': 'No detail found!'}), 401
            
    return jsonify({'status': 'error', 'message': 'Invalid request!'})

@servicesBP.route('/serve-user-payslip/<filename>')
def serve_user_payslip(filename):
    return send_from_directory(app.config['USER_PAYSLIP'], filename)

@servicesBP.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    staffId = get_jwt_identity()
    oldPassword = request.json['oldPassword']
    newPassword = request.json['newPassword']
    print(staffId, oldPassword, newPassword)
    if all([staffId, oldPassword, newPassword]):
        staff_old_password = db_request.get_detail('GET_PASSWORD', (int(staffId),))
        print(staff_old_password)
        if staff_old_password:
            if bcrypt.check_password_hash(staff_old_password[0], oldPassword):
                hashed_password = bcrypt.generate_password_hash(newPassword).decode('utf-8')
                update_password = db_request.update_data('UPDATE_PASSWORD', (staffId, hashed_password))
                if update_password:
                    return jsonify({'message': 'Password updated successfully!'}), 200
                else:
                    return jsonify({'message': 'Failed to update password!'}), 401
            else:
                return jsonify({'message': 'Wrong old password!'}), 401
        else:
            return jsonify({'message': 'No detail found!'}), 401

app.register_blueprint(servicesBP)



#--------------------------------- End Of Service Blueprint ----------------------------------#

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(app.config['PROFILE_FOLDER'], filename)

