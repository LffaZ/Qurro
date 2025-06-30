// Get the microphone icon element
const microphoneIcon = document.getElementById('microphone-icon');

// Track the recording status
let isRecording = false;

// Add click event listener
microphoneIcon.addEventListener('click', function() {
    // Toggle the "recording" class when the microphone is clicked
    isRecording = !isRecording;

    if (isRecording) {
        // Change the microphone icon color to red when recording starts
        microphoneIcon.classList.add('recording');
        
        // Simulate starting recording
        console.log("Recording started...");

    } else {
        // Change the microphone icon color back to normal when recording stops
        microphoneIcon.classList.remove('recording');
        
        // Simulate stopping recording
        console.log("Recording stopped...");

        // Display a success notification after stopping the recording
        createToast('success', 'fa-solid fa-circle-check', 'Recording Finished', 'BISA GAYS ALHAMDULILLAH!!!.');
    }
});

// Function to create a toast notification
function createToast(type, icon, title, text) {
    const notifications = document.querySelector('.notifications');
    let newToast = document.createElement('div');
    newToast.innerHTML = `
        <div class="toast ${type}">
            <i class="${icon}"></i>
            <div class="content">
                <div class="title">${title}</div>
                <span>${text}</span>
            </div>
            <i class="fa-solid fa-xmark" onclick="(this.parentElement).remove()"></i>
        </div>`;
    notifications.appendChild(newToast);
    newToast.timeOut = setTimeout(() => newToast.remove(), 5000); // Remove the toast after 5 seconds
}
