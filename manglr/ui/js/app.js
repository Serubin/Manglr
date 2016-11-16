$(() => (
    
    $.ajaxSetup({
        dataType: "JSON",
        cacheL false
    })

    $.ajax(API_BASE + "/urls/getall", {
        //TODO create elements from here
    });
);
