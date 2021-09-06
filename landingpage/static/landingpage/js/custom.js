let list = document.getElementsByClassName("faq-list")[0]

fetch("/static/data/faqs.json").then(res => {
    res.json().then(items => {
        items.forEach((element, index) => {

            // add the question
            let li = document.createElement("li")
            li.setAttribute("data-aos", "fade-up")
            li.innerHTML = `
                 
                <a data-toggle="collapse" class="collapse" href="#faq-list-${index + 1}">
                    
                <i class="bx bx-help-circle iicon-help"></i>
                ${element.q} 
                    <i class="bx bx-chevron-down icon-show"></i>
                    <i class="bx bx-chevron-up icon-close"></i>
                </a>
                <div id="faq-list-${index + 1}" class="collapse ${index == 0 ? 'show' : 'hide'}" data-parent=".faq-list">
                    
                </div>
                `

            list.appendChild(li)

            // add the answer
            let html = document.getElementById(`faq-list-${index + 1}`)
            let paragraphs = element.a.split("\n")

            paragraphs.forEach(i => {
                let ell = document.createElement("p")
                ell.innerText = i
                html.appendChild(ell)
            })
        });
    })
})