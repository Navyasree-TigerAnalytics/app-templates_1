import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ItemsService } from 'src/app/services/items.service';

@Component({
  selector: 'app-edititems',
  templateUrl: './edititems.component.html',
  styleUrls: ['./edititems.component.css']
})
export class EdititemsComponent {

  angForm: FormGroup
  item_id: any;
  constructor(private fb: FormBuilder,
    private itemsservice: ItemsService, private route: Router,
    private activatedRoute: ActivatedRoute) {
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

    this.activatedRoute.paramMap.subscribe(paramId => {
      this.item_id = paramId.get('item_id');
      console.log(this.item_id);

      this.itemsservice.getitem(this.item_id).subscribe(data => {
        this.angForm.patchValue(data);
      })
    });
  }
  postdata(data: any) {
    this.itemsservice.edititem(this.item_id, this.angForm.value).subscribe(data => {
      this.route.navigate(['itemslist']);

    })
  }

}
