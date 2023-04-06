import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { AppRoutingModule } from './app-routing.module';
import { MatTableModule } from '@angular/material/table';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon'
import { AppComponent } from './app.component';
import { AdditemsComponent } from './components/additems/additems.component';
import { ItemslistComponent } from './components/itemslist/itemslist.component';
import { EdititemsComponent } from './components/edititems/edititems.component';
import { HttpClientModule } from '@angular/common/http';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule } from '@angular/forms';
import { ItemdetailsComponent } from './components/itemdetails/itemdetails.component';
import { FormsModule } from '@angular/forms';



@NgModule({
  declarations: [
    AppComponent,
    AdditemsComponent,
    ItemslistComponent,
    EdititemsComponent,
    ItemdetailsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    CommonModule,
    NoopAnimationsModule,
    MatTableModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatInputModule,
    MatIconModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
