let searchTimeout;
function debounceSearch(form) {
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    form.submit();
  }, 1000); // 1000 мс = 1 секунда
}