// Since Seeding in Mongo is done in alphabetical order... It's is important to keep
// file names alphabetically ordered, if multiple files are to be run.

db.usage_statistics.drop();
db.usage_statistics.insertMany([
  {
    ip_address: "153.23.21.120",
    email: "Hey Sam, Don't forget our discussion of last night. I'm sure you'll do the right choice. Cheers from your best",
    tag: "ham",
    date_sent: "2023-08-14T18:25:43.511Z"
  },
  {
    ip_address: "14.213.121.92",
    email: "Congratulations. You won 55 packs of beers for only $999.99. Take it quick.",
    tag: "spam",
    date_sent: "2023-08-11T09:25:43.511Z"
  }
])