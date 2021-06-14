var test;

fetch('footer.html', {
		headers: {
			'Content-Type': 'text/plain',
		}
	})
	.then(response => response.text()
	.then(data => document.getElementById('footer').innerHTML = data));
