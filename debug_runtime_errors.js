// Debug script to check for common runtime errors
console.log("🔍 Checking for runtime errors...");

// Check if all required modules are available
try {
  const React = require('react');
  console.log("✅ React available");
} catch (e) {
  console.error("❌ React not available:", e.message);
}

try {
  const styled = require('styled-components');
  console.log("✅ Styled-components available");
} catch (e) {
  console.error("❌ Styled-components not available:", e.message);
}

try {
  const { FaImage } = require('react-icons/fa');
  console.log("✅ React-icons available");
} catch (e) {
  console.error("❌ React-icons not available:", e.message);
}

// Check if backend is running
fetch('http://localhost:5000/api/health')
  .then(response => response.json())
  .then(data => {
    console.log("✅ Backend is running:", data);
  })
  .catch(error => {
    console.error("❌ Backend not accessible:", error.message);
  });

console.log("🔍 Runtime error check complete");


















