function alert_message(message_icon,message_title)
{
    Swal.fire(
    {
        background:'linear-gradient(to bottom, #68EACC 0%, #497BE8 100%)',
        confirmButtonColor:'#a6c4f1',
        icon: message_icon,
        title: message_title,
          //text: 'Something went wrong!',:
    }
    )
}
