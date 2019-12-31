// Load papers
d3.json("http://localhost:8619/?get=raw").then(function(papers) {
    init_papers(papers)
})

// Bound paper information
d3.select("#update_button")
    .on("click", () => update_paper())

// Init papers
function init_papers(papers) {
    console.log(papers)

    // Work on paper_list
    paper_list = d3.select("#left_bar")
        .selectAll("ol")
        .data(papers)
        .enter()

    // Add <li> for each paper
    paper_list.append("li")
        .text((d) => d.title)
        .attr("id", (d) => "li-" + d.uid)
        .attr("class", (d) => "li-papers")

    // Bound click event
    .on("click", function(d) {
        // Report
        console.log(d.title)
        console.log(d.doi)
        console.log(d.rawpath)
        console.log(d.uid)

        d3.selectAll(".li-papers")
            .attr("style", "color:gray")
        d3.select("#li-" + d.uid)
            .attr("style", "color:red")

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
}

// Update paper information
function update_paper() {
    console.log('-----------------------------------------------------------')
    console.log("[Title]    " + get_textarea("paper_title"))
    console.log("[DOI]      " + get_textarea("paper_doi"))
    console.log("[Keywords] " + get_textarea("paper_keywords"))
    console.log("[Comments] " + get_textarea("paper_comments"))
}

// Safety get value of textarea
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

console.log('Done')