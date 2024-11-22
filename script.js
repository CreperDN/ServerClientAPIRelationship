var button = document.getElementById('button');
button.addEventListener("click", setCity);
var city;

function setCity() {
    document.getElementById('result').innerHTML = '';
    city = document.getElementById('city').value;
    const url = '/api/';
    async function postData() {
        if (!city.trim()) {
            document.getElementById('error').innerHTML = 'Користувач не ввів назву';
        }
        else{
            try {
                var response = await fetch(url+city);
            }catch {
                response = await fetch_again2(2);
            }
            try{
            if (response.status == 404){
                document.getElementById('error').innerHTML = 'Інформація відсутня';
            }                
            const data = await response.json();
            return data;}
            catch{
                return undefined;
            }
            }
        }

    aResponse = postData();

    aResponse
        .then((data) => {
            if (data) {
                    data.forEach(element => {
                        document.getElementById('error').innerHTML = "";
                        document.getElementById('result').innerHTML += '<h3>' + element.display_name + '</h3>';
                        Object.entries(element).forEach(entry => {
                            document.getElementById('result').innerHTML += '<h5>' + entry[0] + ':' + entry[1] + '</h5>';})
                })
            } 
        })

        async function fetch_again2(i) {
            await new Promise(resolve => setTimeout(resolve, 3000)); 
            document.getElementById('error').innerHTML = "Сталася помилка з'єднання. Зробимо ще " + i + " спроб";
            try{
            var response = await fetch(url + city);}
            catch{
                if (i > 0){
                    return fetch_again2(i - 1);}
                else {
                    document.getElementById('error').innerHTML = "Не вдалося з'єднатись з сервером";}
            }
        return response
}}
