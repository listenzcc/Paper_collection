// Load papers
d3.json("http://localhost:8619/?get=raw").then(function(raw) {
    init_papers(raw)
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

        // Append rawpath session
        d3.select("#paper_path")
            .text(d.rawpath)

        // Append title session
        d3.select("#paper_title")
            .attr("placeholder", d.title)

        // Append doi session
        d3.select("#paper_doi")
            .attr("placeholder", d.doi)

        // Append uid session
        d3.select("#paper_uid")
            .text(d.uid)
    })
}

// Update paper information
function update_paper() {
    title = get_textarea("paper_title")
    doi = get_textarea("paper_doi")
    keywords = get_textarea("paper_keywords")
    comments = get_textarea("paper_comments")
    rawpath = d3.select("#paper_path").text()
    uid = d3.select("#paper_uid").text()
    url = "http://localhost:8619/?set=custom" +
        ",uid=" + uid +
        ",rawpath=" + rawpath +
        ",title=" + title +
        ",keywords=" + keywords +
        ",comments=" + comments
    url = `http://localhost:8619/?set=custom&uid=${uid}&rawpath=${rawpath}&title=${title}&keywords=${keywords}&comments=${comments}`


    console.log('-----------------------------------------------------------')
    console.log("[Title]    " + title)
    console.log("[DOI]      " + doi)
    console.log("[Keywords] " + keywords)
    console.log("[Comments] " + comments)

    d3.json(url).then(function(custom) {
        console.log(custom)
    })
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