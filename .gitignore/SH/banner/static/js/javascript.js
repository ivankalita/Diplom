$("#clearform").on('click', function() {
    var temp = this.form.main_search.value;
    $("form").trigger("reset");
    $("input[name='main_search']").val(temp)
});