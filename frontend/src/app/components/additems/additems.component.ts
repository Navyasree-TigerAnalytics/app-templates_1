import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ItemsService } from 'src/app/services/items.service';
import { Items } from 'src/app/items'

@Component({
  selector: 'app-additems',
  templateUrl: './additems.component.html',
  styleUrls: ['./additems.component.css']
})
export class AdditemsComponent implements OnInit {

  angForm: FormGroup
  constructor(private fb: FormBuilder,
    private itemsservice: ItemsService, private route: Router) {
    this.angForm = this.fb.group({
      item_id: ['', Validators.required],
      item_code: ['', Validators.required],
      item_name: ['', Validators.required],
      recommender_flag: ['', Validators.required],
      scenario_planner_flag: ['', Validators.required],
      category_id: ['', Validators.required],
      promo_type_id: ['', Validators.required],
      promo_type_code: ['', Validators.required],
      n_store: ['', Validators.required],
      active: ['', Validators.required],
    })
  }
  ngOnInit(): void {

  }
  postdata(data: any) {
    this.itemsservice.additem(this.angForm.value).subscribe(data => {
      this.route.navigate(['itemslist']);

    })
  }

}
