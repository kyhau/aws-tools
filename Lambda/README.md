# Lambda Tricks

- [Hit the 6MB Lambda payload limit? Here’s what you can do](
  https://theburningmonk.com/2020/04/hit-the-6mb-lambda-payload-limit-heres-what-you-can-do/)
  by Yan Cui on 2020-04-09

- [Shave 99.93% off your Lambda bill with this one weird trick](
  https://medium.com/@hichaelmart/shave-99-93-off-your-lambda-bill-with-this-one-weird-trick-33c0acebb2ea)
  by Michael Hart on 2019-12-10
  - The init stage has the same performance as a 1792 MB Lambda, even if we’re only running a 128 MB one.
  - Technically you can do up to 10 seconds of work before it starts getting included in the billed duration. 
  - Also, you'll always have to pay something for the handler execution - the minimum billed execution time is 100ms.
 