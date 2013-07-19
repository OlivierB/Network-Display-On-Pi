$(document).ready(function() {

	$('.suppr').click(function() {
		var id = this.id.substr(5);
		console.log(id);

		if (confirm("You are about to delete this module, do you want to continue ?")) {
			$.ajax({
				type: "POST",
				url: "/admin/sql/delete_module.php",
				data: {
					'id': id
				},
				success: function(){
					location.reload();
				}
			});
		}
	});
});