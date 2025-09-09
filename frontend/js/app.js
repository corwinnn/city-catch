const input = document.getElementById('city-input');
const resultDiv = document.getElementById('result');

function lookup(city) {
  const base = window.API_BASE || '';
  const url = base ? `${base}/api/city?name=${encodeURIComponent(city)}` :
                     `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(city)}?origin=*`;
  fetch(url)
    .then(r => r.json())
    .then(data => {
      if (data.error) {
        resultDiv.textContent = 'City not found.';
      } else {
        const title = data.title || data.displaytitle || city;
        const extract = data.extract || data.description || '';
        resultDiv.innerHTML = `<h2>${title}</h2><p>${extract}</p>`;
      }
    })
    .catch(() => {
      resultDiv.textContent = 'Error retrieving data.';
    });
}

input.addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    const city = input.value.trim();
    if (city) {
      lookup(city);
    }
  }
});
