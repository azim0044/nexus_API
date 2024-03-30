let latitude_hidden = document.getElementById('student-latitude');
let longitude_hidden = document.getElementById('student-longitude');
let form = document.getElementById('attendance-form');
let student_ic_no = document.getElementById('student-ic-no');
let modalElement = document.getElementById('exampleModal');
let modal = new bootstrap.Modal(modalElement);
let event_id;

async function check_out_time(id) {

    try {
        const response = await fetch('/check-out-time', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'event-id': id
            })
        });
        const data = await response.json();
        console.log('Success:', data);
        return data.event_ended;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}

function startCheckIn(id, check_status) {
    event_id = id;
    if (check_status == 'check-in') {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((showPosition) => {
                latitude_hidden.value = showPosition.coords.latitude;
                longitude_hidden.value = showPosition.coords.longitude;

                // Make an AJAX request to the server to check if the location is within the radius
                fetch('/dashboard', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: new URLSearchParams({
                        'student-ic-no': student_ic_no.value,
                        'event-id': event_id,
                        'student-latitude': latitude_hidden.value,
                        'student-longitude': longitude_hidden.value
                    })
                })
                    .then(response => response.text())
                    .then(result => {
                        if (result === 'true') {
                            modal.show();
                            startCamera();
                        } else {
                            let error = document.getElementById('alert-danger');
                            error.innerHTML = 'You are not within the radius of the event !';
                            error.style.display = 'block';
                            setTimeout(function () {
                                error.style.display = 'none';
                            }, 3500);
                        }
                    })
                    .catch(error => console.error('Error:', error));
            },
                (error) => {
                    console.log(error);
                });
        } else {
            result.innerHTML = "Geolocation is not supported by this browser.";
        }

    } else if (check_status == 'check-out') {
        check_out_time(event_id).then(eventEnded => {
            if (eventEnded) {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition((showPosition) => {
                        latitude_hidden.value = showPosition.coords.latitude;
                        longitude_hidden.value = showPosition.coords.longitude;

                        // Make an AJAX request to the server to check if the location is within the radius
                        fetch('/dashboard', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            body: new URLSearchParams({
                                'student-ic-no': student_ic_no.value,
                                'event-id': event_id,
                                'student-latitude': latitude_hidden.value,
                                'student-longitude': longitude_hidden.value
                            })
                        })
                            .then(response => response.text())
                            .then(result => {
                                if (result === 'true') {
                                    modal.show();
                                    startCamera();
                                } else {
                                    let error = document.getElementById('alert-danger');
                                    error.innerHTML = 'You are not within the radius of the event !';
                                    error.style.display = 'block';
                                    setTimeout(function () {
                                        error.style.display = 'none';
                                    }, 3500);
                                }
                            })
                            .catch(error => console.error('Error:', error));
                    },
                        (error) => {
                            console.log(error);
                        });
                } else {
                    result.innerHTML = "Geolocation is not supported by this browser.";
                }
            } else {
                let error = document.getElementById('alert-danger');
                error.innerHTML = 'The event has not ended yet. Please wait until the event has ended !';
                error.style.display = 'block';
                setTimeout(function () {
                    error.style.display = 'none';
                }, 3500);
            }
        });
    }
}

const video = document.querySelector('video');
const canvas = document.querySelector('canvas');
const context = canvas.getContext('2d');
const resultsDiv = document.getElementById('ocr-results');
const box = document.getElementById('box');
const startCameraButton = document.getElementById('start-camera');
let stream;
let beepSound;
let intervalId; // Define intervalId here

function startCamera() {
    document.getElementById('video-container').style.display = 'inline-block';
    beepSound = new Audio("/static/sound/beep.mp3");
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
        .then(s => {
            stream = s;
            video.srcObject = stream;
            video.onloadedmetadata = startProcessing;
        });
}

function stopCamera() {
    stream.getTracks().forEach(track => track.stop());
    document.getElementById('video-container').style.display = 'none';
}

function closeCamera() {
    stopCamera();
    clearInterval(intervalId); // Now intervalId is accessible here
};

function startProcessing() {
    let errorCount = 0;
    intervalId = setInterval(() => {
        // Set canvas size to video's natural size
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        context.drawImage(video, 0, 0, canvas.width, canvas.height); // Draw the video frame to the canvas
        const data = canvas.toDataURL('image/jpeg', 0.1); // Reduce quality to 0.5
        fetch('/verify-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: data })
        })
            .then(response => {
                if (response.status === 200) {
                    clearInterval(intervalId); // Stop the interval
                    // Close the modal and stop the camera
                    // Show success message
                    checkInUser();
                } else if (response.status === 400) {
                    errorCount++;
                    if (errorCount >= 3) {
                        clearInterval(intervalId); // Stop the interval
                        // Close the modal and stop the camera
                        // Show error message
                        modal.hide();
                        let error = document.getElementById('alert-error');
                        closeCamera()
                        stopCamera()
                        error.innerHTML = 'Face Not Recognize !';
                        error.style.display = 'block';
                        setTimeout(function () {
                            error.style.display = 'none';
                        }, 2000);
                    }
                }
                return response.json();
            })

    }, 2000);
}

function checkInUser() {
    // Make an AJAX request to the server to check if the location is within the radius
    fetch('/check-in-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'status': 'check-in',
            'event-id': event_id,
            'student-ic-no': student_ic_no.value
        })
    })
        .then(response => response.json()) // Parse the JSON from the response
        .then(data => {
            // Check the message from the server
            if (data.message === "Check In") {
                modal.hide();
                closeCamera()
                stopCamera()
                // Store a flag in the sessionStorage before reloading the page
                sessionStorage.setItem('showAlert', 'true');
                sessionStorage.setItem('messageType', 'success');
                // Reload the page
                window.location.reload();
            } else if (data.message === "Check Out") {
                modal.hide();
                closeCamera()
                stopCamera()
                // Handle check out
                // You can add your check out logic here
                sessionStorage.setItem('showAlert', 'true');
                sessionStorage.setItem('messageType', 'danger');
                // Reload the page
                window.location.reload();
            } else {
                // Handle the error
                console.error('Error:', data.message);
            }
        })
        .catch(error => {
            // Handle the error
            console.error('Error:', error);
        });
}
// After the page has reloaded, check for the flag in the sessionStorage
window.onload = function () {
    let messageType = sessionStorage.getItem('messageType');
    let showAlert = sessionStorage.getItem('showAlert') === 'true';
    let message, alertElement, beepSound;

    if (showAlert) {
        if (messageType === 'success') {
            alertElement = document.getElementById('alert-success');
            message = 'You Are Successfully Check In !';
            beepSound = new Audio("/static/sound/beep.mp3");

        } else if (messageType === 'danger') {
            alertElement = document.getElementById('alert-success');
            message = 'You Are Successfully Check Out !';
            beepSound = new Audio("/static/sound/beep.mp3");
        }

        if (alertElement) {
            beepSound.play();
            alertElement.innerHTML = message;
            alertElement.style.display = 'block';
            setTimeout(function () {
                alertElement.style.display = 'none';
            }, 2000);
        }

        // Remove the flags from the sessionStorage
        sessionStorage.removeItem('showAlert');
        sessionStorage.removeItem('messageType');
    }
}