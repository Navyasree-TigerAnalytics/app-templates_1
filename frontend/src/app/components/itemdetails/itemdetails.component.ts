import { Component, OnInit } from '@angular/core';
import { Items } from 'src/app/items';
import { ItemsService } from 'src/app/services/items.service';

@Component({
  selector: 'app-itemdetails',
  templateUrl: './itemdetails.component.html',
  styleUrls: ['./itemdetails.component.css']
})
export class ItemdetailsComponent implements OnInit {
  items: any;
  item: Items = {
    item_id: '',
    item_code: '',
    item_name: '',
    recommender_flag: true,
    scenario_planner_flag: true,
    category_id: '',
    promo_type_id: '',
    promo_type_code: '',
    n_store: '',
    active: true,
  };
  displayedColumns = ['item_id', 'item_code', 'item_name', 'recommender_flag', 'scenario_planner_flag', 'category_id', 'promo_type_id', 'promo_type_code', 'n_store', 'active']
  constructor(
    private itemsservice: ItemsService,) { }
  ngOnInit(): void {

  }

  getsingleitem(item_id: any) {
    this.itemsservice.getitem(item_id).
      subscribe((data) => {
        this.items = data;
        this.items = this.items.data;
        console.log(this.items);
      })
  }
}
