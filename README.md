# Time Slicing

Generate a combined image from a timelapse image sequence.

## Usage

Call the `process` function:

```
process('./timelapse/tokyo-tower', './timelapse', n_col=11, reverse=False, offset_begin=100, offset_end=0, angle=30)
```

Parameters:
* folder: where the image sequence is stored.
* out_folder: where to save the output image.
* n_col: number of columns.
* reverse: False -> from 1 to N; True -> from N to 1.
* offset_{begin, end}: ignore the first X images and the last Y images.
* angle: rotate X degrees.



## Example

<img src=https://user-images.githubusercontent.com/6956659/184659096-b10a3c4e-fe49-4d95-a73e-de6fe82fa6b3.jpg width=48%> <img src=https://user-images.githubusercontent.com/6956659/184659128-022f95bb-3490-488a-82bc-b577e9b39fe6.jpg width=48%>
