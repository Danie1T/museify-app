var divOne = document.getElementById("one")
var divSix = document.getElementById("six")
var divAllTime = document.getElementById("alltime")

var divList = [divOne, divSix, divAllTime]

function toggleOne()
{
    toggleDisplay("one")
}

function toggleSix()
{
    toggleDisplay("six")
}

function toggleAllTime()
{
    toggleDisplay("alltime")
}

function toggleDisplay(id)
{
    var divDisplay = document.getElementById(id)

    for (var i = 0; i < 3; i++)
    {
        if (divList[i] === divDisplay)
        {
            divList[i].style.display = "flex";
        }
        else
        {
            divList[i].style.display = "none";
        }
    }
}