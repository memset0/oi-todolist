$("#add-problem-button").click(function(){
	$.post(
		'/api/add_problem',
		{'content': $('#add-problem-textarea').val()}
	).done(function(){
		location.reload();
	});
});

$('#button-download-problem-name').click(function(){
	$.post(
		'/api/download_problem_name'
	).done(function(){
		location.reload();
	});
})