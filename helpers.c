#include "helpers.h"
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
  for (int i = 0; i < height; i++)
  {
      for (int  j = 0; j < width; j++)
      {
          int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0f);
          //hard code average
          image[i][j].rgbtBlue = average;
          image[i][j].rgbtGreen = average;
          image[i][j].rgbtRed = average;
      }
  }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    int widthInterval = floor(width / 2.0f);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < widthInterval; j++)
        {
            //swap current cell with opposite cell; use a temp (leftmost with rightmost)
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][(width - 1) - j];
            image[i][(width - 1) - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //GET TEMP ARRAY!!! SWICTH VALUES LATER
    RGBTRIPLE temp[height][width];
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            //iterate over 3*3 box; top to bottom left to right
            //manages vertical travel
            int averageBlue = 0;
            int averageGreen = 0;
            int averageRed = 0;
            
            float numbersInAvg = 0;

            for(int k = -1; k <= 1; k++)
            {

                for(int l = -1; l <= 1; l++)
                {
                    //if both i and j when modifed stay within bounds of picture
                    if((i + k < height && i + k >= 0) && (j + l < width && j + l >= 0))
                    {
                        //printf("blue avg: %i, green avg: %i, red avg: %i\n",   image[i + k][j + l].rgbtBlue, image[i + k][j + l].rgbtGreen,  image[i + k][j + l].rgbtRed);
                        //add values for averaging
                        averageBlue += image[i + k][j + l].rgbtBlue;
                        averageGreen += image[i + k][j + l].rgbtGreen;
                        averageRed += image[i + k][j + l].rgbtRed;
                        //one more number is added to each average color
                        numbersInAvg++;
                    }
                }
            }
           
            //apply colour averages to our temp while code continues to excecute, this is so each pixel's values can stay consistent wile processing and thus so we can get accurate answers
            temp[i][j].rgbtBlue = round(averageBlue / numbersInAvg);
            temp[i][j].rgbtGreen = round(averageGreen / numbersInAvg);
            temp[i][j].rgbtRed = round(averageRed / numbersInAvg);
            
            //printf("blue avg: %i, green avg: %i, red avg: %i\n",  averageBlue, averageGreen,  averageRed);
        }
    }
    
    //apply new colors to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
