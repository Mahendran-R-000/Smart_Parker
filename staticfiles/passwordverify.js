function checkPassword(form)
{
    var passw=  /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{7,15}$/;
    password1 = form.password.value;
    password2 = form.retypepassword.value;
    if (password1 != password2)
    {
        Swal.fire(
        {
            background:'#fff59d',
            confirmButtonColor:'#0d6efd',
            icon: 'error',
            title: 'Password Mismatch',
            text: 'Please Check your password Once Again',
        }
        )
        return false;
    }
    if (password2.match(passw))
    {
        return true;
    }
    else
    {
        Swal.fire(
        {
            background:'#fff59d',
            confirmButtonColor:'#0d6efd',
            icon: 'error',
            title: 'Password Must be strong',
            text: 'Password is too common,Password should be alphanumeric',
        }
        )
        return false;
        }
}