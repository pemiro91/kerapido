function validateFormIdentidad() {
    var name_bussiness = document.forms["formBussiness"]["name_bussiness"].value;
    var logo_bussiness = document.forms["formBussiness"]["logo_bussiness"].value;
    var portada_bussiness = document.forms["formBussiness"]["portada_bussiness"].value;
    var category_bussiness = document.forms["formBussiness"]["category_bussiness"].value;
    if (name_bussiness === "") {
        alert("El nombre debe ser llenado");
        return false;
    } else if (logo_bussiness === "") {
        alert("Debe agregar un logotipo");
        return false;
    } else if (portada_bussiness === "") {
        alert("Debe agregar una portada");
        return false;
    } else if (category_bussiness === "") {
        alert("Debe seleccionar al menos una categoria");
        return false;
    } else {
        var $active = $('.body .nav-tabs li.active');
        var a = document.getElementById('enlace_servicio'); //or grab it by tagname etc
        a.href = "servicio"
        $active.next().removeClass('disabled');
        $('.nav-tabs > .active').next('li').find('a').trigger('click');
        return true;
    }
}

$('.btnPrevious').click(function () {
    $('.nav-tabs > .active').prev('li').find('a').trigger('click');
});

function validateFormServicio() {
    var services_bussiness = document.forms["formBussiness"]["services_bussiness"].value;
    var frecuencia_bussiness = document.forms["formBussiness"]["frecuencia_bussiness"].value;
    var hour_init_bussiness = document.forms["formBussiness"]["hour_init_bussiness"].value;
    var hour_end_bussiness = document.forms["formBussiness"]["hour_end_bussiness"].value;

    if (services_bussiness === "") {
        alert("Debe seleccionar al menos un servicio");
        return false;
    } else if (frecuencia_bussiness === "") {
        alert("Debe seleccionar al menos un dia de la semana");
        return false;
    } else if (hour_init_bussiness === "") {
        alert("La hora de apertura debe ser llenada");
        return false;
    } else if (hour_end_bussiness === "") {
        alert("La hora de cierre debe ser llenada");
        return false;
    } else {
        var $active = $('.body .nav-tabs li.active');
        var a = document.getElementById('enlace_contacto'); //or grab it by tagname etc
        a.href = "contacto"
        $active.next().removeClass('disabled');
        $('.nav-tabs > .active').next('li').find('a').trigger('click');
        return true;
    }
}

function validateFormContacto() {
    var address_bussiness = document.forms["formBussiness"]["address_bussiness"].value;
    var municipio_bussiness = document.forms["formBussiness"]["municipio_bussiness"].value;
    var phone_bussiness_o = document.forms["formBussiness"]["phone_bussiness_o"].value;

    if (address_bussiness === "") {
        alert("La dirección debe ser llenada");
        return false;
    } else if (municipio_bussiness === "") {
        alert("Debe seleccionar un municipio");
        return false;
    } else if (phone_bussiness_o === "") {
        alert("El teléfono de ser llenado");
        return false;
    } else {
        return true;
    }
}

function validateFormIdentidadEditar() {
    var nombre_bussiness = document.forms["formBussiness"]["nombre"].value;
    var category_bussiness = document.forms["formBussiness"]["category_bussiness"].value;

    if (nombre_bussiness === "") {
        alert("El nombre debe ser llenado");
        return false;
    } else if (category_bussiness === "") {
        alert("Debe seleccionar al menos una categoria");
        return false;
    } else {
        var $active = $('.body .nav-tabs li.active');
        var a = document.getElementById('enlace_servicio'); //or grab it by tagname etc
        a.href = "servicio"
        $active.next().removeClass('disabled');
        $('.nav-tabs > .active').next('li').find('a').trigger('click');
        return true;
    }
}

function validateFormTab() {
    var nombre_bussiness = document.forms["formBussiness"]["nombre"].value;
    var category_bussiness = document.forms["formBussiness"]["category_bussiness"].value;

    if (nombre_bussiness === "") {
        alert("El nombre debe ser llenado");
        return false;
    } else if (category_bussiness === "") {
        alert("Debe seleccionar al menos una categoria");
        return false;
    } else {
        var $active = $('.body .nav-tabs li.active');
        var a = document.getElementById('enlace_servicio_li'); //or grab it by tagname etc
        a.href = "servicio"
        $active.next().removeClass('disabled');
        $('.nav-tabs > .active').next('li').find('a').trigger('click');
        return true;
    }
}