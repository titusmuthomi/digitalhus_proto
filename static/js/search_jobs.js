// $(document).ready(function(){
    // alert("hi")
    const perPage = 2;
    function load_data(currentPage, job_title, location, job_type, search_salary){
        if(!currentPage) {
            currentPage = 1;
        }
        // alert(currentPage)
        $.ajax({
            url: "/search",
            method: "POST",
            data: {
                currentPage: currentPage,
                job_title: job_title,
                location: location,
                job_type: job_type,
                search_salary: search_salary,
            },
            success: function(data){
                $('#filtered').html(data.htmlresponse);
                if (parseInt($('#currentPage').val(), 0) == 1) {
                    $('#prev').prop(
                        "disabled",
                        true
                    );
                };

                if (parseInt($('#currentPage').val(), 0) == parseInt($('#total').val(), 0)) {
                    $('#next').prop(
                        "disabled",
                        true
                    );
                };
                
            }
        });
    }

    function fetch_results() {
        var job_title = $('#search_text').val();
        var location = $('#search_location').val()=="Select Location" ? $('#search_location2').val() : $('#search_location').val();
        var job_type = $('#search_category').val();
        var search_salary = $('#search_salary').val();
        var currentPage = 1;
        if (location === "Select Location") {
            location = null;
        }
        if (job_type === "Job Type") {
            job_type = null;
        }
        if (search_salary  === "Salary Range") {
            search_salary = null;
        }
        // alert(job_type)
        load_data(currentPage, job_title, location, job_type, search_salary);
    }

    $('#search_text').keyup(function(){
        fetch_results();
    });

    $('#search_location').change(function(){
        fetch_results();
    });

    $('#search_location2').change(function(){
        fetch_results();
    });

    $('#search_category').change(function(){
        fetch_results();
    });

    $('#search_salary').change(function(){
        fetch_results();
    });

$(document).ready(function(){
    load_data();
    // $('#paginate').customPaginator({
    //     pageItems:  $('.job_item'),
    // });
});



function prev() {
    var currentPage = parseInt($('#currentPage').val(), 0);
    if (currentPage > 1) {
        load_data(currentPage - 1);
    }
};

function next() {
    var currentPage = parseInt($('#currentPage').val(), 0);
    currentPage += 1
    // if (currentPage <= parseInt($('#total').val(), 0)){
        load_data(currentPage);
    // }
};
function pages(page_no){
    load_data(page_no)
}