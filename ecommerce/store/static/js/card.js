var updateBtnsPay = document.getElementsByClassName('update-payment-methods')
console.log(updateBtnsPay.length)
for (i = 0; i < updateBtnsPay.length; i++) {
	updateBtnsPay[i].addEventListener('click', function(){
		var cardId = this.dataset.card
		var action = this.dataset.action
		console.log('cardId:', cardId, 'Action:', action)
		console.log('USER:', user)

		updateCard(cardId, action)
	})
}

function updateCard(cardId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_card/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'cardId':cardId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}