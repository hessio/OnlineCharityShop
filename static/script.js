const fileInput = document.getElementById('file-input');
const fileLabel = document.getElementById('file-label-span');

fileInput.addEventListener('change', () => {
  const filename = fileInput.value.split('\\').pop();
  fileLabel.textContent = filename || 'Choose file...';
});
