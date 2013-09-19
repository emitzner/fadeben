require 'httparty'
require 'nokogiri'
require 'date'
require 'json'

abort 'usage: ruby nfl.rb [WEEK NUM]' if ARGV.size < 1

resp = HTTParty.get("http://m.nfl.com/scores/reg/#{ARGV.shift}/")
parser = Nokogiri::HTML(resp.body)

year = Time.now.year
games = []

parser.css('h3').each do |header|
  date = header.text
  date.sub!(/\d+th|\d+rd|\d+st|\d+nd/) { |d| d.to_s.to_i }

  # must inject a year since its not provided
  date << " #{date =~ /jan|feb/i ? year + 1 : year}"

  header.next_element.css('li').each do |li|
    datetime = "#{date} #{li.css('.time').text}"

    games.push({
      :home => li.css('.hm span').text,
      :away => li.css('.awy span').text,
      :link => li.css('a').first['href'],
      :date => DateTime.strptime(datetime, "%A, %B %d %Y %I:%M %P %Z").to_time.to_i
               })

  end
end

puts games.to_json
