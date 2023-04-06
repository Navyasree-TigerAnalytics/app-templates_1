import { Component, Input, OnInit } from '@angular/core';
import { ItemsService } from 'src/app/services/items.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Items } from 'src/app/items';

@Component({
  selector: 'app-itemslist',
  templateUrl: './itemslist.component.html',
  styleUrls: ['./itemslist.component.css']
})
export class ItemslistComponent implements OnInit {
  items: any;
  displayedColumns = ['item_id', 'item_code', 'item_name', 'recommender_flag', 'scenario_planner_flag', 'category_id', 'promo_type_id', 'promo_type_code', 'n_store', 'active', 'edit', 'actions']
  constructor(private itemsservice: ItemsService, private router: Router) { }

  ngOnInit(): void {
    this.fetchitems();
  }

  delitem(item_id: any) {
    this.itemsservice.deleteitem(item_id).subscribe(() => {
      this.fetchitems();
    });
  }

  fetchitems() {
    this.itemsservice.itemslist().subscribe((data) => {
      this.items = data;
      this.items = this.items.data;
    })
  }

}
