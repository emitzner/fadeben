require 'httparty'
require 'nokogiri'
require 'json'

resp = HTTParty.get('http://m.nfl.com/scores/reg/1/')
parser = Nokogiri::HTML(resp.body)

games = []
parser.css('h3').each do |header|
  date = header.text

  header.next_element.css('li').each do |li|
    games.push({
      :home => li.css('.awy span').text, 
      :away => li.css('.hm span').text, 
      :link => li.css('a').first['href'], 
                 :date => "#{date} #{li.css('.time').text}"
               })

  end
end

puts games.to_json
