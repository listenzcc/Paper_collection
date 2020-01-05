// Load papers
d3.json("http://localhost:8619/?get=raw").then(function(raw) {
    d3.json("http://localhost:8619/?get=custom").then(function(custom) {
        init_pages(raw)
        init_update_pages(custom)
    })
})

// Bound paper information
d3.select("#update_button")
    .on("click", () => update_custom())

// Init update pages
function init_update_pages(custom) {
    console.log('-- init_update_page --')
    console.log(custom)
    console.log(custom.title)
    for (uid in custom.title) {
        console.log(uid)
        d3.select("#li-" + uid)
            .text("[" + custom.title[uid] + "]")
    }
}

// Init pages
// papers: raw papers read from raw json
function init_pages(papers) {
    console.log(papers)

    // Build paper list on left_bar
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

    // Highlight clicked <li>
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
        update_paper_info(d, custom)
    })

}

// Update paper using custom information
function update_paper_info(d, custom) {
    // Report
    console.log(d.uid)

    // Init paper information
    document.getElementById("paper_title").value = ""
    document.getElementById("paper_doi").value = ""
    document.getElementById("paper_keywords").value = ""
    document.getElementById("paper_comments").value = ""

    // Override paper information with custom
    if (custom.title[d.uid]) {
        document.getElementById("paper_title").value = custom.title[d.uid]
    }
    if (custom.keywords[d.uid]) {
        document.getElementById("paper_keywords").value = custom.keywords[d.uid]
    }
    if (custom.comments[d.uid]) {
        document.getElementById("paper_comments").value = custom.comments[d.uid]
    }
}

// Update custom using paper information
// function update_custom_using_HTTPGET() {
//     uid = document.getElementById("paper_uid").innerHTML
//     url = `http://localhost:8619/?set=custom&uid=${uid}`
//     url += query_from_textarea("paper_title", "&title")
//     url += query_from_textarea("paper_keywords", "&keywords")
//     url += query_from_textarea("paper_comments", "&comments")

//     console.log("Update custom with url:")
//     console.log(url)

//     d3.json(url).then(function(custom) {
//         console.log(custom)
//     })
// }

function update_custom() {
    uid = document.getElementById("paper_uid").innerHTML
    url = `http://localhost:8619/?set=custom&uid=${uid}`
    console.log(url)

    title = query_from_textarea("paper_title", "")

    $.post(url, {
            date: String(new Date()),
            title: title,
            keywords: query_from_textarea("paper_keywords", ""),
            comments: query_from_textarea("paper_comments", "")
        },
        function(data, status) {
            console.log("Update custom with url:")
            console.log(url)
            console.log("Data: " + data + "\nStatus: " + status)
        });

    d3.select("#li-" + uid)
        .text("[" + title + "]")
}

// Safety build query with content in textarea
function query_from_textarea(id, name) {
    // Get DOM by id
    ta = document.getElementById(id)

    if (name) {
        name += "="
    }

    // Return value or placeholder
    if (ta.textLength == 0) {
        return ""
    } else {
        return name + ta.value
    }
}

console.log('Done')