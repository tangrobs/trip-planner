var CSRFToken = $('meta[name="csrf-token"]').attr('content')

$(document).on('click', '#add-button', function(){
    $.ajax({
        url: '/trips/plan/{{trip.id}}/agenda/new',
        success: function(serverResponse) {
        console.log("add day button submitted")
        console.log("this is the serverResponse:", serverResponse)
        $('.tab').html(serverResponse)

        $.ajax({
            url: '/trips/plan/{{trip.id}}/agenda/new/content',
            success: function(serverResponse) {
            console.log("add day button submitted")
            console.log("this is the serverResponse:", serverResponse)
            $('.tabcontents').html('')
            $('.tabcontents').html(serverResponse)
            $('#defaultOpen').click()
            }
        })

        }
    })
})
$(document).on('click', '.tablinks', function(){
    $.ajax({
        url: '/setdaysession/'+ $(this).attr('day'),
        success: console.log('succesfully clicked the button')
    })
    $.ajax({
        url: '/trips/plan/agenda/new/content',
        success: function(serverResponse){
            $('.tabcontents').html(serverResponse)
            console.log('should be working')
        }
    })
    
})
