let list = document.getElementsByClassName("faq-list")[0]

fetch("/static/data/faqs.json").then(res => {
    res.json().then(items => {
        items.forEach((element, index) => {
            let li = document.createElement("li")
            li.setAttribute("data-aos", "fade-up")
            li.innerHTML = `
                <i class="bx bx-help-circle icon-help"></i> 
                <a data-toggle="collapse" class="collapse" href="#faq-list-${index + 1}">
                    ${element.q} 
                    <i class="bx bx-chevron-down icon-show"></i>
                    <i class="bx bx-chevron-up icon-close"></i>
                </a>
                <div id="faq-list-${index + 1}" class="collapse ${index == 0 ? 'show' : 'hide'}" data-parent=".faq-list">
                    
                </div>
                `

            list.appendChild(li)

            let html = document.getElementById(`faq-list-${index + 1}`)
            let paragraphs = element.a.split("\n")

            paragraphs.forEach(i => {
                let ell = document.createElement("p")
                ell.innerText = i
                html.appendChild(ell)
            })

            // html.appendChild(li)
        });
    })
})