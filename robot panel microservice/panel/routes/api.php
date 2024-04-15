<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TextController;

Route::post('/save-text', [TextController::class, 'store']);
Route::get('/get-text', [TextController::class, 'show']);
