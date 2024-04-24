function PostAnswer(answer) {
    fetch('/' + answer, { method: 'POST' })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function GetAnswer(answer) {
    fetch('/next', { method: 'GET' })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Parse the JSON response
        })
        .then(data => {
            // Update the question and answers with the new values
            document.getElementById('question').innerText = data.question;
            document.getElementById('ans1').innerText = data.ans1;
            document.getElementById('ans2').innerText = data.ans2;
            document.getElementById('ans3').innerText = data.ans3;
            document.getElementById('ans4').innerText = data.ans4;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}