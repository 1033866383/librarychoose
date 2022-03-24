import { request } from './server.js'

export const AllLibraryInfo = 
function() {
    return request.get('/seat/alllibraryinfo')
    .then(data=>{return data.data})
}

export const AddLibrary = 
function(param) {
    return request.post('/seat/addlibrary',param)
    .then(data=>{return data.data})
}


export const AllSeatInfo = 
function(id, library) {
	if(id && !library){
		return request.get('/seat/allseatinfo?id='+id)
		.then(data=>{return data.data})
	}else if(!id && library){
		return request.get('/seat/allseatinfo?library='+library)
		.then(data=>{return data.data})
	}else{
		return request.get('/seat/allseatinfo?id='+id+"&library="+library)
		.then(data=>{return data.data})
	}
    
}

export const AddSeat = 
function(param) {
    return request.post('/seat/addseat?library',param)
    .then(data=>{return data.data})
}
