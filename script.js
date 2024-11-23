document.getElementById('numberForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const number = document.getElementById('numberInput').value;
    const url = `/api/${number}`;
    let attemptCount = 0;

    function fetchData () {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Помилка запиту до сервера');
                }
                return response.text();
            })
            .then(data => {
                document.getElementById('facts').innerHTML = data;
            })
            .catch(error => {
                attemptCount++;
                if (attemptCount < 3) {
                    setTimeout(fetchData, 10000);
                } else {
                    document.getElementById('facts').innerHTML = `<p>Помилка: ${error}</p>`;
                }
            });
    };

    fetchData();
});