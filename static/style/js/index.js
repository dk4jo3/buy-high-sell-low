// asyng function to fetch
async function getData() {
    const results = await fetch('/../static/style/js/priceData.json');
    const dataObj = await results.json();
    console.log(dataObj);


    // shorten Object.keys function
    function getKeys(n) {
        return Object.keys(n);
    }

    // get keys and push into a new array

    let objKeys = [];
    
    // -1 since the last object is time
    for (i = 0; i < getKeys(dataObj).length - 1; i++) {
        objKeys.push(getKeys(dataObj)[i]);
    }

    // .map the keys to get html content and generate html content
          
    const cards = objKeys.map(key => {
        return ` <div class="col-md-4">
                <div class="card">
                    <img class="card-img-top" src="${dataObj[key].img}" alt="Card image cap">
                    <div class="card-body">
                        <h2 class="card-title">US$ ${dataObj[key].price}</h2>
                        <hr>
                        <p class="card-text">$ ${dataObj[key].unitDif >= 0 ? `+` : ``}${dataObj[key].unitDif} &nbsp;/&nbsp; ${dataObj[key].percDif >= 0 ? `+` : ``}${dataObj[key].percDif} % <br><span class="vs-info">vs. Coinbase</span></p>
                        <a href="${dataObj[key].url}" target="_blank" class="stretched-link"></a>
                    </div>
                </div>
            </div>`
    }).join('');

    const cardRow = document.querySelector('.card-row');
    const timeRow = document.querySelector('.donate-row .col-sm-12');
    timeRow.textContent = `Last update: ${dataObj['time']['currentTime']}`
    cardRow.innerHTML = cards;

}

getData();
