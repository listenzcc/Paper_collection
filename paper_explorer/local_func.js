d3.json("http://localhost:8619/?|file=../paper_jsons/papers.json").then(function(papers) {
    console.log(papers)
    d3.select("#left_bar")
        .append("ol")
        .selectAll("ol")
        .data(papers)
        .enter()
        .append("li")
        .text((d) => d.title)
        .on("click", function(d) {
            console.log(d.title)
            console.log(d.doi)
            console.log(d.rawpath)

            // Display the paper
            d3.select("#pdf_iframe")
                .attr("src", d.rawpath)

            // Append title session
            d3.select("#paper_title")
                .attr("placeholder", d.title)

            // Append doi session
            d3.select("#paper_doi")
                .attr("placeholder", d.doi)

            // Append rawpath session
            d3.select("#paper_path")
                .text(d.rawpath)
        })
})

d3.select("#update_button")
    .on("click", function() {
        console.log("[Title] " + get_textarea("paper_title"))
    })

function get_textarea(id) {
    // Get DOM by id
    ta = document.getElementById(id)

    // Return value or placeholder
    if (ta.textLength == 0) {
        return ta.placeholder
    } else {
        return ta.value
    }
}

d3.select("#comment")
    .attr("oninput", "auto_grow(this)")

function auto_grow(element) {
    console.log(element.scrollHeight)
    console.log(element.clientHeight)
    if (element.scrollHeight < 500) {
        if (element.scrollHeight > element.clientHeight) {
            element.style.height = (element.scrollHeight) + "px"
        }
    }
}

console.log('Done')