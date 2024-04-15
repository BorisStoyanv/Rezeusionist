<?php

namespace App\Http\Controllers;

use App\Models\Text;
use Illuminate\Http\Request;

class TextController extends Controller
{
    public function store(Request $request)
    {
        $text = Text::firstOrNew(); 
        $text->content = $request->input('content');
        $text->save();

        return response()->json(['message' => 'Text saved successfully'], 201);
    }

    public function show()
    {
        $text = Text::firstOrNew();

        if (!$text->exists) {
            return response()->json(['message' => 'No text found'], 404);
        }

        return response()->json($text->content);
    }

}