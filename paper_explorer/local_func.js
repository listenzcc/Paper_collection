// Load papers
d3.json("http://localhost:8619/?get=raw").then(function(raw) {
    init_papers_raw(raw)
})

// Bound paper information
d3.select("#update_button")
    .on("click", () => update_custom())

// Init papers
function init_papers_raw(papers) {
    console.log(papers)

    // Work on paper_list
    paper_list = d3.select("#left_bar")
        .append("ol")
        .selectAll()
        .data(papers)
        .enter()
        // Add <li> for each paper
        .append("li")
        .text((d) => d.title)
        .attr("id", (d) => "li-" + d.uid)
        .attr("class", (d) => "li-papers")

    // Bound click event
    .on("click", function(d) {
        display_paper(d)
    })
}

// Display paper
function display_paper(d) {
    // Report
    console.log(d.title)
    console.log(d.doi)
    console.log(d.rawpath)
    console.log(d.uid)
    console.log(d.fname)

    d3.selectAll(".li-papers")
        .attr("style", "color:gray")
    d3.select("#li-" + d.uid)
        .attr("style", "color:red")

    // Display the paper
    src = `http://localhost:8619/?get=pdf&fname=${d.fname}`
    d3.select("#pdf_iframe")
        .attr("src", src)

    // Refresh rawpath session
    d3.select("#paper_path")
        .text(d.rawpath)

    // Refresh title session
    d3.select("#paper_title")
        .attr("placeholder", d.title)

    // Refresh doi session
    d3.select("#paper_doi")
        .attr("placeholder", d.doi)

    // Append uid session
    d3.select("#paper_uid")
        .text(d.uid)

    d3.json("http://localhost:8619/?get=custom").then(function(custom) {
        update_paper(d, custom)
    })

}

// Update paper using custom information
function update_paper(d, custom) {
    // Report
    console.log(d.uid)

    // Override paper title
    document.getElementById("paper_title").value = ""
    if (custom.title[d.uid]) {
        document.getElementById("paper_title").value = custom.title[d.uid]
    }
    document.getElementById("paper_doi").value = ""
    document.getElementById("paper_keywords").value = ""
    document.getElementById("paper_comments").value = ""
}

// Update custom using paper information
function update_custom() {
    uid = document.getElementById("paper_uid").innerHTML
    url = `http://localhost:8619/?set=custom&uid=${uid}`
    url += query_from_textarea("paper_title", "&title")
    url += query_from_textarea("paper_keywords", "&keywords")
    url += query_from_textarea("paper_comments", "&comments")

    console.log("Update custom with url:")
    console.log(url)

    d3.json(url).then(function(custom) {
        console.log(custom)
    })
}

// Safety build query with content in textarea
function query_from_textarea(id, name) {
    // Get DOM by id
    ta = document.getElementById(id)

    // Return value or placeholder
    if (ta.textLength == 0) {
        return ""
    } else {
        return name + "=" + ta.value
    }
}

console.log('Done')