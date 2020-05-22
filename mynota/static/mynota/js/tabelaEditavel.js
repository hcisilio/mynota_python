function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(function () {
	// $("#result_list").dblclick(function () {
	$("#result_list").on("dblclick", ".editavel", function(){
		var conteudoOriginal = $(this).text();
		$(this).addClass("celulaEmEdicao");
		$(this).html("<input type='text' size='3' value='" + conteudoOriginal + "' />");
		$(this).children().first().select();
		//$(this).children().first().focus();
		$(this).children().first().keypress(function (e) {
			if (e.which == 13) {
				var conteudoNovo = $(this).val();
				if ( conteudoNovo != "" && conteudoNovo != conteudoOriginal && conteudoNovo <= 10 ) {
					var objeto = $(this);
					$.ajax ({
						type:"POST",
						url:"/notas/lancar_nota/",
						dataType: "json",
						data:{
							csrfmiddlewaretoken: getCookie('csrftoken'),
							aluno_id: $(this).parents('tr').children().first().attr('title'),
							modulo_id: $(this).parent().attr('title'),
							valor: conteudoNovo
						},
						success:function(result){
							objeto.parent().html(conteudoNovo);
							$('body').append(result);
						},
						error:function(xhr){
							alert(xhr.responseText);
						}
					});
				}
				else {
					$(this).parent().html(conteudoOriginal);
				};
			}
		});
		$(this).children().first().blur(function(){
			$(this).parent().text(conteudoOriginal);
			$(this).parent().removeClass("celulaEmEdicao");
		});
	});
});