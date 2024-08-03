document.getElementById('converter-form').addEventListener('input', function(e) {
    e.preventDefault();

    const amount = document.getElementById('amount').value;
    const resultDiv = document.getElementById('result');

    const rate = 6.68031791/1000;
    const ErrorRate = 0.0119695182/1000;
    const result = amount * rate;
    const resultError = amount * ErrorRate;
    resultDiv.innerHTML = `${amount} KZT = ${result.toFixed(2)} ± ${resultError.toFixed(2)} BYN`;
});
