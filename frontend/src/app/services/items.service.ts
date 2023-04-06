import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Items } from '../items'
@Injectable({
  providedIn: 'root'
})
export class ItemsService {
  Api_Url = 'http://localhost:8000/common/items';

  constructor(private http: HttpClient) { }

  itemslist() {
    return this.http.get<Items>(this.Api_Url)
  }
  additem(data: any) {
    return this.http.post<Items>(this.Api_Url, data);
  }

  edititem(item_id: number, data: any) {
    return this.http.put<Items>(this.Api_Url + '/' + item_id + '/', data);
  }

  deleteitem(item_id: any) {
    console.log(item_id);
    return this.http.delete<Items>(this.Api_Url + '/' + item_id + '/');

  }

  getitem(item_id: number) {
    return this.http.get<Items>(this.Api_Url + '/' + item_id + '/');
  }
}
