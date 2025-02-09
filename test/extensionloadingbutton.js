const startBtn = document.getElementById('startBtn');
const diagnosticBtn = document.getElementById('diagnosticBtn');
let isRunning = false; // Flag to track if diagnostics are running

startBtn.addEventListener('click', startDiagnostics);
diagnosticBtn.addEventListener('click', stopDiagnostics); // Make loading button clickable

function startDiagnostics() {
    if (isRunning) return; // Prevent multiple starts
    isRunning = true;
    startBtn.classList.add('hidden');
    diagnosticBtn.classList.remove('hidden');
}

function stopDiagnostics() {
    if (!isRunning) return; // Prevent stopping if not running
    isRunning = false;

    diagnosticBtn.classList.add('hidden');
    startBtn.classList.remove('hidden');

    // Add your logic to actually stop the diagnostics (e.g., abort an API call)
    console.log("Diagnostics stopped.");
}