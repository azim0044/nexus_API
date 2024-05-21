import datetime 

class DatabaseRequest:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_detail(self, query_type, data):
        cur = self.mysql.connection.cursor()

        if query_type == 'LOGIN_STAFF':
            STAFF_ID = data[0]
            COMPANY_CODE = data[1]

            sql_query = """
               SELECT * FROM users WHERE userId = %s AND userCompanyId = %s
            """

            cur.execute(sql_query, (STAFF_ID, COMPANY_CODE))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'LOGIN_ADMIN':
            USERNAME = data[0]
            COMPANY_CODE = data[1]

            sql_query = """
               SELECT * FROM admin WHERE adminUsername = %s AND adminCompanyId = %s
            """

            cur.execute(sql_query, (USERNAME, COMPANY_CODE))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'HOME_PAGE':
            STAFF_ID = data[0]
            
            sql_query = """
               SELECT userFullName, userReference FROM users WHERE userId = %s
            """

            cur.execute(sql_query, (STAFF_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'PERSONAL_DETAIL':
            STAFF_ID = data[0]
            
            sql_query = """
               SELECT userId, userFullName, userPosition, userRace, userNationality, userReligion  FROM users WHERE userId = %s
            """

            cur.execute(sql_query, (STAFF_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'GET_ADDRESS':
            STAFF_ID = data[0]
            sql_query = """
               SELECT * FROM useraddress WHERE userId = %s
            """
            cur.execute(sql_query, (STAFF_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'GET_CONTACT':
            STAFF_ID = data[0]
            sql_query = """
               SELECT * FROM usercontactinformation WHERE userId = %s
            """
            cur.execute(sql_query, (STAFF_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'OLD_EDUCATION':
            STAFF_ID = data[0]
            sql_query = """
               SELECT educationProof FROM usereducation WHERE userId = %s
            """
            cur.execute(sql_query, (STAFF_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'GET_EDUCATION':
            STAFF_ID = data[0]
            sql_query = """
               SELECT * FROM usereducation WHERE userId = %s
            """
            cur.execute(sql_query, (STAFF_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'GET_CLAIMS':
            STAFF_ID = data[0]
            sql_query = """
               SELECT * FROM userClaim WHERE userId = %s
            """
            cur.execute(sql_query, (STAFF_ID,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts
        
        if query_type == 'GET_LEAVES':
            STAFF_ID = data[0]
            sql_query = """
               SELECT * FROM userleave WHERE userId = %s
            """
            cur.execute(sql_query, (STAFF_ID,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts
        
        if query_type == 'GET_SERVICES_DESK':
            STAFF_ID = data[0]
            sql_query = """
               SELECT * FROM userservicedesk WHERE userId = %s
            """
            cur.execute(sql_query, (STAFF_ID,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts
        
        if query_type == 'CHECK_COMPANY_CODE':
            COMPANY_ID = data[0]
            sql_query = """
               SELECT * FROM companydetail WHERE companyId = %s
            """
            cur.execute(sql_query, (COMPANY_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'CHECK_USER_ID':
            USER_ID = data[0]
            sql_query = """
               SELECT * FROM users WHERE userId = %s
            """
            cur.execute(sql_query, (USER_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'CHECK_ADMIN_USERNAME':
            USERNAME = data[0]
            sql_query = """
               SELECT * FROM admin WHERE adminUsername = %s
            """
            cur.execute(sql_query, (USERNAME,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'GET_ALL_PENDING_LEAVES':
            COMPANY_CODE = data[0]
            sql_query = """
                SELECT l.*, u.userFullName 
                FROM `userleave` AS l
                INNER JOIN users AS u ON l.userId = u.userId
                WHERE l.leaveStatus IN ('pending', 'rejected')
                AND u.userCompanyId = %s;
            """
            cur.execute(sql_query, (COMPANY_CODE,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts
        
        if query_type == 'GET_ALL_LEAVES':
            COMPANY_CODE = data[0]
            sql_query = """
                SELECT l.*, u.userFullName 
                FROM `userleave` AS l
                INNER JOIN users AS u ON l.userId = u.userId
                WHERE u.userCompanyId = %s;
            """
            cur.execute(sql_query, (COMPANY_CODE,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts

        if query_type == 'GET_ALL_PENDING_CLAIMS':
            COMPANY_CODE = data[0]
            sql_query = """
                SELECT l.*, u.userFullName 
                FROM `userclaim` AS l
                INNER JOIN users AS u ON l.userId = u.userId
                WHERE l.claimStatus IN ('pending', 'rejected')
                AND u.userCompanyId = %s;
            """
            cur.execute(sql_query, (COMPANY_CODE,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts

        if query_type == 'GET_ALL_CLAIMS':
            COMPANY_CODE = data[0]
            sql_query = """
                SELECT l.*, u.userFullName 
                FROM `userclaim` AS l
                INNER JOIN users AS u ON l.userId = u.userId
                WHERE u.userCompanyId = %s;
            """
            cur.execute(sql_query, (COMPANY_CODE,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts
        
        if query_type == 'CHECK_STAFF_ID':
            userId = data[0]
            
            sql_query = """
                SELECT userId FROM users WHERE userId = %s;
            """

            cur.execute(sql_query, (userId,))
            result = cur.fetchone()
            cur.close()
            return result
        
        if query_type == 'GET_STAFF_LIST':
            COMPANY_CODE = data[0]
            sql_query = """
                SELECT 
                u.*,
                cd.companyName,
                COALESCE(ua.address1, 'Not Yet Updated') AS address1,
                COALESCE(ua.address2, 'Not Yet Updated') AS address2,
                COALESCE(ua.addressCity, 'Not Yet Updated') AS addressCity,
                COALESCE(ua.addressPostcode, 'Not Yet Updated') AS addressPostcode,
                COALESCE(ua.addressRegion, 'Not Yet Updated') AS addressRegion,
                COALESCE(uc.userEmail, 'Not Yet Updated') AS userEmail,
                COALESCE(uc.userPhone, 'Not Yet Updated') AS userPhone,
                COALESCE(uc.emergencyName, 'Not Yet Updated') AS emergencyName,
                COALESCE(uc.emergencyPhone, 'Not Yet Updated') AS emergencyPhone,
                COALESCE(uc.emergencyRelay, 'Not Yet Updated') AS emergencyRelay,
                COALESCE(ue.userEducation, 'Not Yet Updated') AS userEducation,
                COALESCE(ue.userUniversity, 'Not Yet Updated') AS userUniversity,
                COALESCE(ue.userYear, 'Not Yet Updated') AS userYear,
                COALESCE(ue.userResult, 'Not Yet Updated') AS userResult,
                COALESCE(ue.educationProof, 'Not Yet Updated') AS educationProof
                FROM 
                `users` AS u
                LEFT JOIN 
                useraddress AS ua ON u.userId = ua.userId
                LEFT JOIN
                usercontactinformation AS uc ON u.userId = uc.userId
                LEFT JOIN
                usereducation AS ue ON u.userId = ue.userId
                LEFT JOIN
                companydetail AS cd ON u.userCompanyId = cd.companyId
                WHERE 
                u.userCompanyId = %s;
            """
            cur.execute(sql_query, (COMPANY_CODE,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts
        
        if query_type == 'GET_ALL_PENDING_SERVICE':
            COMPANY_CODE = data[0]
            sql_query = """
                SELECT l.*, u.userFullName 
                FROM `userservicedesk` AS l
                INNER JOIN users AS u ON l.userId = u.userId
                WHERE l.serviceStatus = 'pending'
                AND u.userCompanyId = %s;
            """
            cur.execute(sql_query, (COMPANY_CODE,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts
        
        if query_type == 'GET_ALL_SERVICE':
            COMPANY_CODE = data[0]
            sql_query = """
                SELECT l.*, u.userFullName 
                FROM `userservicedesk` AS l
                INNER JOIN users AS u ON l.userId = u.userId
                WHERE l.serviceStatus = 'done'
                AND u.userCompanyId = %s;
            """
            cur.execute(sql_query, (COMPANY_CODE,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts

        if query_type == 'GET_REF_IMAGE':
            STAFF_ID = data[0]

            sql_query = """
               SELECT userReference FROM users WHERE userId = %s
            """

            cur.execute(sql_query, (STAFF_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'CHECK_ATTENDANCE':
            staffId = data[0]
            attendanceDate = data[1]

            sql_query = """
                SELECT * FROM userattendance WHERE userId = %s AND DATE(attendanceDate) = %s
            """

            cur.execute(sql_query, (staffId, attendanceDate))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'GET_ALL_USER':
            companyCode = data[0]

            sql_query = """
                SELECT userId, userFullName, userPosition FROM users WHERE userCompanyId = %s
            """

            cur.execute(sql_query, (companyCode,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts
        
        if query_type == 'GET_MEMO':
            memoTo = data[0]
            memoStatus = data[1]

            sql_query = """
            SELECT m.*, a.adminFullname, u.userFullName
            FROM memo as m
            INNER JOIN admin as a ON m.adminId = a.adminId
            INNER JOIN users as u ON m.memoTo = u.userId
            WHERE m.memoTo = %s AND m.memoStatus = %s;
            """

            cur.execute(sql_query, (memoTo, memoStatus))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts
        
        if query_type == 'GET_USER_ATTENDANCE':
            userId = data[0]

            sql_query = """
            SELECT *
            FROM userattendance
            WHERE userId = %s;
            """

            cur.execute(sql_query, (userId,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            
            # Organize results by month
            user_attendance_by_month = {}
            for result in results_dicts:
                attendance_date = result['attendanceDate']
                month = attendance_date.strftime('%Y-%m')
                if month not in user_attendance_by_month:
                    user_attendance_by_month[month] = []
                user_attendance_by_month[month].append(result)

            return user_attendance_by_month

        if query_type == 'GET_PASSWORD':
            userId = data[0]

            sql_query = """
            SELECT userPassword
            FROM users
            WHERE userId = %s;
            """

            cur.execute(sql_query, (userId,))
            result = cur.fetchone()
            cur.close()
            return result
        
        if query_type == 'TEST':
            companyId = data[0]

            # Query to get user details
            sql_query_user = """
            SELECT * 
            FROM users
            WHERE companyId = %s;
            """
            cur.execute(sql_query_user, (companyId,))
            user_results = cur.fetchall()
            user_column_names = [desc[0] for desc in cur.description] if cur.description else []
            user_dicts = [dict(zip(user_column_names, result)) for result in user_results] if user_column_names and user_results else {}

            # Query to get user attendance
            sql_query_attendance = """
            SELECT *
            FROM userattendance;
            """
            cur.execute(sql_query_attendance)
            attendance_results = cur.fetchall()
            attendance_column_names = [desc[0] for desc in cur.description] if cur.description else []
            attendance_results_dicts = [dict(zip(attendance_column_names, result)) for result in attendance_results] if attendance_column_names and attendance_results else []
            cur.close()

            # Organize attendance results by user and month
            user_attendance = {}
            for user in user_dicts:
                user_attendance[user['userId']] = {'users_detail': user, 'attendance_detail': {}}
                for result in attendance_results_dicts:
                    if result['userId'] == user['userId']:
                        attendance_date = result['attendanceDate']
                        month = attendance_date.strftime('%Y-%m')
                        if month not in user_attendance[user['userId']]['attendance_detail']:
                            user_attendance[user['userId']]['attendance_detail'][month] = []
                        user_attendance[user['userId']]['attendance_detail'][month].append(result)

            # Return user details and attendance
            return user_attendance
        
        if query_type == 'GET_USER_DETAIL':
            STAFF_ID = data[0]

            sql_query = """
               SELECT * FROM users WHERE userId = %s 
            """

            cur.execute(sql_query, (STAFF_ID,))
            result = cur.fetchone()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            result_dict = dict(zip(column_names, result)) if column_names and result else {}
            cur.close()
            return result_dict
        
        if query_type == 'GET_USER_ATTENDANCE_REPORT':
            userId = data[0]
            selected_month = data[1]

            sql_query = """
            SELECT *
            FROM userattendance
            WHERE userId = %s AND DATE_FORMAT(attendanceDate, '%%Y-%%m') = %s;
            """

            cur.execute(sql_query, (userId, selected_month))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()

            return results_dicts
        
        if query_type == 'GET_PAYSLIP':
            userId = data[0]
            print('hit')
            sql_query = """
            SELECT *
            FROM userpayslip
            WHERE userId = %s;
            """

            cur.execute(sql_query, (userId,))
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description] if cur.description else []
            results_dicts = [dict(zip(column_names, result)) for result in results] if column_names and results else []
            cur.close()
            return results_dicts

    def insert_data(self, query_type, data):
        cur = self.mysql.connection.cursor()

        if query_type == 'INSERT_STAFF':
            
            try:
                FULLNAME = data[0]
                USERNAME = data[1]
                PASSWORD = data[2]
                COMPANY_CODE = data[3]

                sql_query = """
                    INSERT INTO admin (adminFullname, adminUsername, adminPassword, adminCompanyId)
                    VALUES (%s, %s, %s, %s);
                """
                cur.execute(sql_query, (FULLNAME, USERNAME, PASSWORD, COMPANY_CODE))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'INSERT_COMPANY':
            
            try:
                COMPANY_NAME = data[0]
                COMPANY_CODE = data[1]

                sql_query = """
                    INSERT INTO companydetail (companyName, companyId)
                    VALUES (%s, %s);
                """
                cur.execute(sql_query, (COMPANY_NAME, COMPANY_CODE))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'INSERT_ADDRESS':
            
            try:
                staffId = data[0]
                address1 = data[1]
                address2 = data[2]
                city = data[3]
                postcode = data[4]
                region = data[5]

                sql_query = """
                    INSERT INTO useraddress (userId, address1, address2, addressCity, addressPostcode, addressRegion)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql_query, (staffId, address1, address2, city, postcode, region))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False

        if query_type == 'INSERT_CONTACT':
            
            try:
                staffId = data[0]
                userEmail = data[1]
                userPhone = data[2]
                emergencryName = data[3]
                emergencyPhone = data[4]
                emergencyRelationship = data[5]


                sql_query = """
                    INSERT INTO usercontactinformation (userId, userEmail, userPhone, emergencyName, emergencyPhone, emergencyRelay)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql_query, (staffId, userEmail, userPhone, emergencryName, emergencyPhone, emergencyRelationship))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'INSERT_EDUCATION':
            
            try:
                staffId = data[0]
                highestEducation = data[1]
                educationPlace = data[2]
                educationYear = data[3]
                educationResult = data[4]
                educationProof = data[5]

                sql_query = """
                    INSERT INTO usereducation (userId, userEducation, userUniversity, userYear, userResult, educationProof)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql_query, (staffId, highestEducation, educationPlace, educationYear, educationResult, educationProof))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'INSERT_CLAIM':
            
            try:
                staffId = data[0]
                claimGroupName = data[1]
                claimName = data[2]
                claimReceiptNo = data[3]
                claimAmount = data[4]
                claimProof = data[5]

                sql_query = """
                    INSERT INTO userclaim (userId, claimGroupName, claimName, claimReceiptNo, claimAmount, claimProof)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql_query, (staffId, claimGroupName, claimName, claimReceiptNo, claimAmount, claimProof))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'INSERT_LEAVE':
            
            try:
                staffId = data[0]
                leaveReason = data[1]
                leaveStart = data[2]
                leaveEnd = data[3]
                leaveDuration = data[4]
                leaveProof = data[5]

                sql_query = """
                    INSERT INTO userleave (userId, leaveReason, leaveStart, leaveEnd, leaveDuration, leaveProof)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql_query, (staffId, leaveReason, leaveStart, leaveEnd, leaveDuration, leaveProof))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
        
        if query_type == 'INSERT_SERVICE_DESK':
            
            try:
                staffId = data[0]
                serviceProblem = data[1]
                serviceAttachment = data[2]

                sql_query = """
                    INSERT INTO userservicedesk (userId, serviceProblem, serviceAttachment)
                    VALUES (%s, %s, %s);
                """
                cur.execute(sql_query, (staffId, serviceProblem, serviceAttachment))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'INSERT_USERS':
            
            try:
                userId = data[0]
                companyCode = data[1]
                userFullName = data[2]
                userPosition = data[3]
                userRace = data[4]
                userNationality = data[5]
                userReligion = data[6]
                userPassword = data[7]
                refImage = data[8]
        


                sql_query = """
                    INSERT INTO users (userId, userCompanyId, userFullName, userPosition, userRace, userNationality, userReligion, userPassword, userReference)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql_query, (userId, companyCode, userFullName, userPosition, userRace, userNationality, userReligion, userPassword, refImage))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False

        if query_type == 'INSERT_ATTENDANCE':
            try:
                staffId = data[0]
                timeIn = data[1]
                timeLate = data[2]
                attendanceStatus = data[3]

                sql_query = """
                    INSERT INTO userattendance (userId, timeIn, timeLate, attendanceStatus)
                    VALUES (%s, %s, %s, %s);
                """
                cur.execute(sql_query, (staffId, timeIn, timeLate, attendanceStatus))
                self.mysql.connection.commit()

                cur.execute("SELECT * FROM userattendance WHERE attendanceId = LAST_INSERT_ID();")
                last_row = cur.fetchone()
                column_names = [desc[0] for desc in cur.description] if cur.description else []
                result_dict = dict(zip(column_names, last_row)) if column_names and last_row else {}
                cur.close()
                result_dict['attendanceDate'] = result_dict['attendanceDate'].isoformat()
                result_dict['timeIn'] = str(result_dict['timeIn']).split(':')[:2]
                result_dict['timeOut'] = str(result_dict['timeOut']).split(':')[:2]

                # Join hours and minutes with a colon
                result_dict['timeIn'] = ':'.join(result_dict['timeIn'])
                result_dict['timeOut'] = ':'.join(result_dict['timeOut'])
                result_dict['timeLate'] = str(result_dict['timeLate']).split(':')[:2]
                result_dict['overtime'] = str(result_dict['overtime']).split(':')[:2]
                result_dict['timeLate'] = ':'.join(result_dict['timeLate'])
                result_dict['overtime'] = ':'.join(result_dict['overtime'])
                return result_dict

            except Exception as e:
                print(e)
                return False
        
        if query_type == 'INSERT_ANNOUNCEMENT':
            try:
                adminId = data[0]
                memoTo = data[1]
                memoSubject = data[2]
                memoDetail = data[3]

                sql_query = """
                    INSERT INTO memo (adminId, memoTo, memoSubject, memoDetail)
                    VALUES (%s, %s, %s, %s);
                """
                cur.execute(sql_query, (adminId, memoTo, memoSubject, memoDetail))
                self.mysql.connection.commit()
                cur.close()
                return True

            except Exception as e:
                print(e)
                return False
   
        if query_type == 'INSERT_PAYSLIP':
            try:
                userId = data[0]
                fileName = data[1]
                paySlipMonth = data[2]

                sql_query = """
                    INSERT INTO userpayslip (userId, fileName, paySlipMonth)
                    VALUES (%s, %s, %s);
                """
                cur.execute(sql_query, (userId, fileName, paySlipMonth))
                self.mysql.connection.commit()
                cur.close()
                return True
            
            except Exception as e:
                print(e)
                return False
            
    def update_data(self, query_type, data):
        cur = self.mysql.connection.cursor()

        if query_type == 'UPDATE_ADDRESS':
            try:
                staffId = data[0]
                address1 = data[1]
                address2 = data[2]
                city = data[3]
                postcode = data[4]
                region = data[5]
                sql_query = """
                    UPDATE useraddress 
                    SET address1 = %s, address2 = %s, addressCity = %s, addressPostcode = %s,
                    addressRegion = %s
                    WHERE userId = %s;
                """
                cur.execute(sql_query, (address1, address2, city, postcode, region, staffId))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'UPDATE_CONTACT':
            try:
                staffId = data[0]
                userEmail = data[1]
                userPhone = data[2]
                emergencryName = data[3]
                emergencyPhone = data[4]
                emergencyRelationship = data[5]
                
                sql_query = """
                    UPDATE usercontactinformation
                    SET userEmail = %s, userPhone = %s, emergencyName = %s, emergencyPhone = %s, emergencyRelay = %s
                    WHERE userId = %s;
                """
                cur.execute(sql_query, (userEmail, userPhone, emergencryName, emergencyPhone, emergencyRelationship, staffId))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False

        if query_type == 'UPDATE_EDUCATION':
            try:
                staffId = data[0]
                highestEducation = data[1]
                educationPlace = data[2]
                educationYear = data[3]
                educationResult = data[4]
                educationProof = data[5]
                
                sql_query = """
                    UPDATE usereducation
                    SET userEducation = %s, userUniversity = %s, userYear = %s, userResult = %s, educationProof = %s
                    WHERE userId = %s;
                """
                cur.execute(sql_query, (highestEducation, educationPlace, educationYear, educationResult, educationProof, staffId))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'UPDATE_LEAVE':
            try:
                leaveId = data[0]
                leaveStatus = data[1]
                
                sql_query = """
                    UPDATE userleave 
                    SET leaveStatus = %s
                    WHERE leaveId = %s;
                """
                cur.execute(sql_query, (leaveStatus, leaveId))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'UPDATE_CLAIM':
            try:
                claimId = data[0]
                claimStatus = data[1]
                
                sql_query = """
                    UPDATE userClaim 
                    SET claimStatus = %s
                    WHERE claimId = %s;
                """
                cur.execute(sql_query, (claimStatus, claimId))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False

        if query_type == 'UPDATE_SERVICE_DESK':
            try:
                serviceId = data[0]
                serviceNote = data[1]
                serviceStatus = data[2]
                
                sql_query = """
                    UPDATE userservicedesk 
                    SET serviceNote = %s, serviceStatus = %s
                    WHERE serviceId = %s;
                """
                cur.execute(sql_query, (serviceNote, serviceStatus, serviceId))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'UPDATE_ATTENDANCE':
            try:
                staffId = data[0]
                attendanceDate = data[1]
                timeOut = data[2]
                overtime = data[3]
                overtimeStatus = data[4]

                sql_query = """
                    UPDATE userattendance
                    SET timeOut = %s, overtime = %s, overtimeStatus = %s
                    WHERE userId = %s AND DATE(attendanceDate) = %s;
                """
                cur.execute(sql_query, (timeOut, overtime, overtimeStatus, staffId, attendanceDate))
                self.mysql.connection.commit()

                # Fetch the updated row
                cur.execute("SELECT * FROM userattendance WHERE userId = %s AND DATE(attendanceDate) = %s;", (staffId, attendanceDate))
                last_row = cur.fetchone()
                column_names = [desc[0] for desc in cur.description] if cur.description else []
                result_dict = dict(zip(column_names, last_row)) if column_names and last_row else {}
                cur.close()

                # Convert datetime.date and datetime.timedelta objects to strings
                result_dict['attendanceDate'] = result_dict['attendanceDate'].isoformat()
                result_dict['timeIn'] = str(result_dict['timeIn']).split(':')[:2]
                result_dict['timeOut'] = str(result_dict['timeOut']).split(':')[:2]

                # Join hours and minutes with a colon
                result_dict['timeIn'] = ':'.join(result_dict['timeIn'])
                result_dict['timeOut'] = ':'.join(result_dict['timeOut'])
                result_dict['timeLate'] = str(result_dict['timeLate']).split(':')[:2]
                result_dict['overtime'] = str(result_dict['overtime']).split(':')[:2]
                result_dict['timeLate'] = ':'.join(result_dict['timeLate'])
                result_dict['overtime'] = ':'.join(result_dict['overtime'])
                return result_dict
            except Exception as e:
                print(e)
                return False
                
        if query_type == 'UPDATE_MEMO':
            try:
                memoId = data[0]
                memoStatus = 'done'
                
                sql_query = """
                    UPDATE memo 
                    SET memoStatus = %s
                    WHERE memoId = %s;
                """
                cur.execute(sql_query, (memoStatus, memoId))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False
            
        if query_type == 'UPDATE_PASSWORD':
            try:
                userId = data[0]
                newPassword = data[1]
                
                sql_query = """
                    UPDATE users 
                    SET userPassword = %s
                    WHERE userId = %s;
                """
                cur.execute(sql_query, (newPassword, userId))
                self.mysql.connection.commit()
                cur.close()
                return True
            except Exception as e:
                print(e)
                return False

    def delete_data(self, query_type, data):
        cur = self.mysql.connection.cursor()

   
   
   