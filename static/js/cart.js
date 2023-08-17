var updatebtn=document.getElementsByClassName("update-cart")

for(var i=0;i<updatebtn.length;i++)
{
    updatebtn[i].addEventListener('click',function(){
        var productid=this.dataset.product
        var action=this.dataset.action
        console.log('product',productid,'action',action)
        if(user==='AnonymousUser')
        {
            addCookieItem(productid,action)
        }
        else
        {
            updateUserOrder(productid,action)
        }
    })
}

function addCookieItem(productid,action)
{
    console.log("Not logged in ....")
    if(action=='add')
    {
        if(cart[productid]==undefined)
        {
            cart[productid]={'quantity':1}
        }
        else
        {
            cart[productid]['quantity']+=1;
        }
    }

    if(action=='remove')
    {
        cart[productid]['quantity']-=1;
        if(cart[productid]['quantity']<=0)
        {
            console.log('Remove Item')
            delete cart[productid]
        }
    }
    console.log('Cart:',cart)
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}
function updateUserOrder(productid,action)
{
    var url='/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId':productid,'action':action})
    })
    .then((response)=>
    {
        return response.json()
    })
    .then((data)=>
    {
        console.log('data:',data)
        location.reload(true)
    })
}