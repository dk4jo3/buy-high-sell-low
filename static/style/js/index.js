// asyng function to fetch
async function getData() {

    const results = await fetch('priceData.json');
    const dataObj = await results.json();
    
    // get keys and push into a new array, and remove the last one (time)
    let objKeys = Object.keys(dataObj).filter(key => key !== 'time');
    
    let objSubKeys = Object.keys(dataObj[objKeys[0]]);
    // it should all be the same, or add a check for that.
              
    // function to poop out html content, take object and key array as the parameters
    function exportCard(arr, object) {
        const content = arr.map(key => {
        return ` <div class="col-md-4">
                <div class="card">
                    <img class="card-img-top" src="${object[key].img}" alt="Card image cap">
                    <div class="card-body">
                        <h2 class="card-title">US$ ${object[key].price}</h2>
                        <hr>
                        <p class="card-text">$ ${object[key].unitDif >= 0 ? `+` : ``}${object[key].unitDif} &nbsp;/&nbsp; ${object[key].percDif >= 0 ? `+` : ``}${object[key].percDif} % <br><span class="vs-info">vs. Coinbase</span></p>
                        <a href="${object[key].url}" target="_blank" class="stretched-link"></a>
                    </div>
                </div>
            </div>`
    }).join('');
        return content;
    }
    
    //loop for objKey to select html elements and assign exportCard function to them.
    objKeys.forEach((key) => {
        window[key+'CardRow'] = document.querySelector(`.${key}-card-row`);
        //btcCardRow = document.querySelector('.btc-card-row')
        
        window[key+'CardRow'].innerHTML = exportCard(objSubKeys, dataObj[key])
        //btcCardRow.innerHTML = exportCard(objSubKeys, dataObg['btc'])
    })
    
 
    const timeRow = document.querySelector('.donate-row .time');
    timeRow.textContent = `Last update: ${dataObj['time']['currentTime']}`

}

getData();

