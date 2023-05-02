

function run(flag) {
    var url = ""
    var timeInterval = 0
    if(flag == "auto") {
        var timeInterval = $("#auto_interval").val()
    }
    if(flag == "manual") {
        var url = $("#dropdown_btn").attr("data-val")
    }

    console.log(flag, url, timeInterval)
    $("#toast-body").text("実行中...")
    $('.toast').toast('show');

    $.post(
        "/run",
        {
            "flag": flag,
            "interval": timeInterval,
            "url": url
        },
        (res) => {
            console.log(res.status)
            if(res.status == "rerun 5min") {
                $("#toast-body").text("現在終了していないプロセスがありますので、5分後にもう一度お試しください。")
            }else if(res.status == "started") {
                $("#toast-body").text("始めました")
            }else if(res.status == "running") {
                $("#toast-body").text("現在実行中です。")
            }
            $(".toast").toast('show')
        }
    )
}

function stop(flag) {
    console.log(flag)
    $("#toast-body").text("停止中")
    $(".toast").toast('show')
    $.post(
        "/stop",
        {
            "flag": flag,
            "data": "stop"
        },
        (res) => {
            console.log(res.status)
            if(res.status == "stopped") {
                $("#toast-body").text("停止")
            }
            $(".toast").toast('show')
        }
    )
}


$(document).ready(() => {
    $("#auto_run").click((e) => {
        e.preventDefault()
        run("auto")
    })

    $("#manual_run").click((e) => {
        e.preventDefault()
        run("manual")
    })

    $("#auto_stop").click((e) => {
        e.preventDefault()
        stop("auto")
    })

    $("#manual_stop").click((e) => {
        e.preventDefault()
        stop("manual")
    })
    let dropDownItems = document.querySelectorAll(".dropdown-item")
    for(let i = 0; i < dropDownItems.length; i ++) {
        dropDownItems[i].addEventListener("click", (e) => {
            itemText = e.target.innerText
            dataVal = $(e.target).attr("data-val")
            $("#dropdown_btn").text(itemText);
            $("#dropdown_btn").attr("data-val", dataVal);
        })
    }
})
