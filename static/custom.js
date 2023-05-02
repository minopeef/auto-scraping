
function run(flag) {
    var url = ""
    var timeInterval = 0
    if(flag == "auto") {
        var timeInterval = $("#auto_interval").val()
    }
    if(flag == "manual") {
        var url = $("#manual_url").val()
    }

    console.log(flag, url, timeInterval)

    $.post(
        "/run",
        {
            "flag": flag,
            "interval": timeInterval,
            "url": url
        },
        (res) => {
            console.log(res)
        }
    )
}

function stop(flag) {
    console.log(flag)
    $.post(
        "/stop",
        {
            "data": "stop"
        },
        (res) => {
            // console.log(res)
        }
    )
}



$(document).ready(() => {
    $("#auto_run").click(() => {
        run("auto")
    })

    $("#manual_run").click(() => {
        run("manual")
    })

    $("#auto_stop").click(() => {
        stop("auto")
    })

    $("#manual_stop").click(() => {
        stop("manual")
    })
})
