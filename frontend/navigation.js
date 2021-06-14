//
//  navigation.js
//  Flowa
//
//  Created by Adam Lewczuk on 2021-06-14.
//  Copyright 2021 Adam Lewczuk. All rights reserved.
//

// NOT USED: The navigation on top of each page can be fetched dynamically
fetch('navigation.html', {
		headers: {
			'Content-Type': 'text/plain',
		}
	})
	.then(response => response.text()
		.then(data => document.getElementById('content').insertAdjacentHTML('beforebegin', data)));
