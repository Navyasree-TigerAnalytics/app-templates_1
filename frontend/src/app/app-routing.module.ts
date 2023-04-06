import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdditemsComponent } from './components/additems/additems.component';
import { EdititemsComponent } from './components/edititems/edititems.component';
import { ItemdetailsComponent } from './components/itemdetails/itemdetails.component';
import { ItemslistComponent } from './components/itemslist/itemslist.component';

const routes: Routes = [
  { path: 'itemslist', component: ItemslistComponent },
  { path: 'additem', component: AdditemsComponent },
  { path: 'edit/:item_id', component: EdititemsComponent },
  { path: 'itemsdetails', component: ItemdetailsComponent },
  { path: 'itemsdetails/:item_id', component: ItemdetailsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
