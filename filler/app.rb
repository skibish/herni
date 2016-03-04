require 'bundler'
Bundler.require

set :port, ENV['PORT'] || 9494
set :bind, '0.0.0.0'
logic_port = ENV['LOGIC_PORT'] || 4567

products = [
  {
    name: "snickers",
    price: 0.80
  },
  {
    name: "cola",
    price: 1.00
  },
  {
    name: "water",
    price: 0.75
  },
  {
    name: "orange juice",
    price: 1.00
  },
  {
    name: "unknown juice",
    price: 0.65
  },
  {
    name: "milk",
    price: 0.85
  },
  {
    name: "Semki",
    price: 0.77
  },
  {
    name: "nuts",
    price: 1.20
  },
  {
    name: "waffels",
    price: 1.10
  },
  {
    name: "banana",
    price: 0.25
  },
  {
    name: "potato",
    price: 0.50
  },
  {
    name: "poison",
    price: 0.45
  }
]

post '/initial_fill' do
  content_type :json

  # get JSON from body
  data = JSON.parse(request.body.read.to_s)
  slots = data["slots"]
  capacity = data["capacity"]
  product_list = []

  # create list of products
  for i in 0..slots-1
    index = i % products.length

    product_list.push({
      id: index,
      name: products[index][:name],
      price: products[index][:price],
      slot: i,
      count: capacity
    })
  end

  # render it
  {products: product_list}.to_json

end

post '/empty' do
  content_type :json
  clnt = HTTPClient.new

  # get JSON from body
  data = JSON.parse(request.body.read.to_s)

  url = "http://#{request.ip}:#{logic_port}/slot_refill"
  index = data['product_id']
  d = {
    product: {
      id: index,
      name: products[index][:name],
      price: products[index][:price],
      slot: data['slot'],
      count: data['capacity']
    }
  }

  # {product: {id: 1, name: "twix", price: 1.00, slot: 1, count: 10 }}

  clnt.post_async(url, d.to_json, {'Content-Type' => 'application/json'})

  {}.to_json

end
