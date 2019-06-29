$("#add-problem-button").click(function(){
	$.post(
		'/api/add_problem',
		{ 'content': $('#add-problem-textarea').val() }
	).complete(function() {
		alert('complete');
		location.reload();
	});
});